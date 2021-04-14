#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

routines for querying the registry

"""
NODELIST = [{'identifier': 'ivo://vamdc/dijon-methane-lines',
             'name': 'MeCaSDa - Methane Calculated Spectroscopic Database',
             'url': u'http://vamdc.icb.cnrs.fr/mecasda-12.07/tap/'},
            {'identifier': 'ivo://vamdc/cdms/vamdc-tap-dev',
             'name': 'CDMS: VAMDC-TAP service (xsams 1.0)',
             'url': u'http://cdms.ph1.uni-koeln.de/cdms/tap/'},
            {'identifier': 'ivo://vamdc/UDFA',
             'name': 'UMIST Database for Astrochemistry',
             'url': u'http://star.pst.qub.ac.uk/sne/umist3/tap/'},
            {'identifier': 'ivo://vamdc/vald/uu/django',
             'name': 'VALD (atoms)',
             'url': u'http://vald.astro.uu.se/atoms-12.07/tap/'},
            {'identifier': 'ivo://vamdc/chianti/django',
             'name': 'Chianti',
             'url': u'http://ag02.ast.cam.ac.uk/chianti-dev/tap/'},
            {'identifier': 'ivo://vamdc/ghosst',
             'name': 'TAP-XSAMS for GhoSST database',
             'url': u'http://ghosst.osug.fr/vamdc/tap/'},
            {'identifier': 'ivo://vamdc/reims-ethylene',
             'name': 'ECaSDa - Ethene Calculated Spectroscopic Database',
             'url': u'http://vamdc.univ-reims.fr/ecasda-12.07/tap/'},
            {'identifier': 'ivo://vamdc/smpo-sample',
             'name': 'GSMA Reims S&MPO',
             'url': u'http://vamdc.univ-reims.fr/smpo12/tap/'},
            {'identifier': 'ivo://vamdc/hitran',
             'name': 'HITRAN-UCL resource',
             'url': u'http://vamdc.mssl.ucl.ac.uk/node/hitran/tap/'},
            {'identifier': 'ivo://vamdc/basecol/vamdc-tap-dev',
             'name': 'BASECOL: development VAMDC-TAP interface',
             'url': u'http://dev.vamdc.org/basecol/tapservice_12_07/TAP/'},
            {'identifier': 'ivo://vamdc/KIDA/vamdc-tap-12.07',
             'name': 'KIDA: 12.07 VAMDC-TAP interface',
             'url': u'http://dev.vamdc.org/kida/tapservice_12_07/TAP/'},
            {'identifier': 'ivo://vamdc/jpl/vamdc-tap-dev',
             'name': 'JPL: VAMDC-TAP service (xsams 1.0)',
             'url': u'http://cdms.ph1.uni-koeln.de/jpl/tap/'},
            {'identifier': 'ivo://vamdc/TOPbase/tap-xsams-12.07',
             'name': 'TOPbase : VAMDC-TAP interface (12.07 version)',
             'url': u'http://topbase.obspm.fr/12.07/vamdc/tap/'},
            {'identifier': 'ivo://vamdc/TIPbase/tap-xsams-12.07',
             'name': 'TIPbase : VAMDC-TAP interface (12.07 version)',
             'url': u'http://tipbase.obspm.fr/12.07/vamdc/tap/'},
            {'identifier': 'ivo://vamdc/stark-b/tap-xsams-12.07',
             'name': 'Stark-b',
             'url': u'http://stark-b.obspm.fr/12.07/vamdc/tap/'},
            {'identifier': 'ivo://vamdc/OACatania/LASP1207',
             'name': 'OACT - LASP Database - N1207',
             'url': u'http://dblasp.oact.inaf.it/node1207/OACT/tap/'},
            {'identifier': 'ivo://vamdc/cdsd-296-xsams1',
             'name': 'Carbon Dioxide Spectroscopic Databank 296K (VAMDC-TAP)',
             'url': u'http://lts.iao.ru/node/cdsd-296-xsams1/tap/'},
            {'identifier': 'ivo://vamdc/cdsd-1000-xsams1',
             'name': 'Carbon Dioxide Spectroscopic Databank 1000K (VAMDC-TAP)',
             'url': u'http://lts.iao.ru/node/cdsd-1000-xsams1/tap/'},
            {'identifier': 'ivo://vamdc/cdsd-4000-xsams1',
             'name': 'Carbon Dioxide Spectroscopic Databank 4000K (VAMDC-TAP)',
             'url': u'http://lts.iao.ru/node/cdsd-4000-xsams1/tap/'},
            {'identifier': 'ivo://vamdc/RADAM',
             'name': 'RADAM',
             'url': u'http://193.55.130.154/tap/'}]

for node in NODELIST:
    # HACK: these are all _strictly required_ but none are included above...
    node['referenceUrl'] = node['url']
    node['maintainer'] = 'none'
    node['returnables'] = {'returnable': None}

def getNodeList():

    return NODELIST



if __name__ == '__main__':
    print getNodeList()
