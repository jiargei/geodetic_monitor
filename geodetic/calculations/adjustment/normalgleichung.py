#/bin/python

import logging
import scipy
import scipy.linalg

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def covariance2(n, wR, ws, wz, l):
    """

    :param n:
    :param wR:
    :param ws:
    :param wz:
    :param l:
    :return:
    """
    SLL = scipy.mat(scipy.eye(n * 3))
    for i in range(n):
        # SLL[3*i  ,3*i  ] = SLL[3*i  ,3*i  ]*(wR)**1  # Hz
        # SLL[3*i+1,3*i+1] = SLL[3*i+1,3*i+1]*(wz)**1  # V
        SLL[3 * i + 2, 3 * i + 2] *= (ws + 2 * l[3 * i] * 1e-06) ** 2  # Sd
    return SLL


def covariance(n, ws, wR, wz, l):
    """

    :param n:
    :param ws:
    :param wR:
    :param wz:
    :param l:
    :return:
    """
    SLL = scipy.mat(scipy.eye(n * 3))
    for i in range(n):
        SLL[3 * i, 3 * i] *= (ws + 2 * l[3 * i] * 1e-06) ** 2  # Sd
        SLL[3 * i + 1, 3 * i + 1] *= wR ** 2  # Hz
        SLL[3 * i + 2, 3 * i + 2] *= wz ** 2  # V
    return SLL


def normalgleichung(A, P, l):
    """
    n ... Anzahl der Beobachtungen
    u ... Anzahl der Unbekannten

    :param A: Designmatrix
    :type A: scipy.array(n,u)
    :param P: Gewichtsmatrix a priori
    :type P: scipy.array(n,n)
    :param l: Vektor der Beobachtungen
    :type l: scipy.array(n,1)
    :rtype: tuple(xx,vv,Qxx,Qll,Qlld,Qvv,s02p,Probe)
    :return: Ergebnisse des Ausgleichs nach kleinsten Quadraten
    """
    logger.debug(A.shape)
    logger.debug(P.shape)
    logger.debug(l.shape)

    AT = scipy.transpose(A)
    N = scipy.dot(scipy.dot(AT, P), A)
    Qxx = scipy.linalg.pinv(N)

    # LU Decomposition
    # PP, LL, UU = scipy.linalg.lu(N)
    # Qxx = scipy.dot(scipy.linalg.inv(UU), scipy.dot(scipy.linalg.inv(LL), scipy.transpose(PP)))

    n = scipy.dot(scipy.dot(AT, P), l)

    xx = scipy.dot(Qxx, n)

    vv = scipy.dot(A, xx) - l
    Qll = scipy.linalg.inv(P)

    #Qlld = scipy.dot(UPPER)
    Qlld = scipy.dot(scipy.dot(A, Qxx), AT)
    Qvv = Qll - Qlld
    # rr   = scipy.array([float(scipy.sqrt(scipy.diag(Qvv)[i])) for i in range(len(vv))])

    """Verprobung"""
    vTPv = scipy.dot(scipy.dot(scipy.transpose(vv), P), vv)

    lTPl = scipy.dot(scipy.dot(scipy.transpose(l), P), l)
    nTx = scipy.dot(scipy.transpose(n), xx)

    Probe = vTPv - (lTPl - nTx)

    # print "Verbrobung: %e"%float(Probe)

    r = (A.shape[0] - A.shape[1])

    if r < 0:
        logger.warn("Not enough observations to solve")
        s02p = -9999.9999
    elif r == 0:
        logger.debug("No redundancy given")
        s02p = 0.
    else:
        s02p = vTPv / r

    # print vTPv, A.shape

    return [xx, vv, Qxx, Qll, Qlld, Qvv, s02p, Probe]


def gen_design_plane(Pi, Pk):
    """

    :param Pi:
    :param Pk:
    :return:
    """
    xi, yi, zi = Pi.as_list()
    xk, yk, zk = Pk.as_list()

    # partial derivatives Distance
    dS_dxi = (1.0 * xi - 1.0 * xk) * scipy.sqrt((-xi + xk) ** 2 + (-yi + yk) ** 2)
    dS_dyi = (1.0 * yi - 1.0 * yk) * scipy.sqrt((-xi + xk) ** 2 + (-yi + yk) ** 2)
    dS_doi = 0

    dR_dxi = -1 / ((-yi + yk) * ((-xi + xk) ** 2 / (-yi + yk) ** 2 + 1))
    dR_dyi = (-xi + xk) / ((-yi + yk) ** 2 * ((-xi + xk) ** 2 / (-yi + yk) ** 2 + 1))
    dR_doi = -1

    return scipy.array([[dR_dxi, dR_dyi, dR_doi],
                        [dS_dxi, dS_dyi, dS_doi]])


def gen_design_height(Pi, Pk):
    """

    :param Pi:
    :param Pk:
    :return:
    """
    pass