#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zhoujiebing
@contact: zhoujiebing@maimiaotech.com
@date: 2012-11-06 10:29
@version: 0.0.0
@license: Copyright maimiaotech.com
@copyright: Copyright maimiaotech.com

"""
import os
import sys
import datetime
if __name__ == '__main__':
    sys.path.append('../../')

from CommonTools.send_tools import send_email_with_text, send_sms, DIRECTOR
from CommonTools.logger import logger
from DataAnalysis.conf.settings import CURRENT_DIR
from DataAnalysis.analysis.analysis_campaign_simple import analysis_campaign_simple
from DataAnalysis.analysis.analysis_campaign_complex import analysis_campaign_complex
from DataAnalysis.analysis.analysis_campaign_horizontal import analysis_campaign_horizontal

def analysis_campaign(syb_file, bd_file):
    content = ''
    content += analysis_campaign_complex(syb_file, '省油宝长尾计划')
    content += analysis_campaign_complex(syb_file, '省油宝加力计划')
    content += analysis_campaign_complex(syb_file, '其他计划(省油宝)')
    content += analysis_campaign_complex(bd_file, '北斗专属计划')
    content += analysis_campaign_simple(syb_file)
    content += analysis_campaign_horizontal(syb_file)
    return content

def analysis_campaign_script():
    today = str(datetime.date.today())
    yesterday = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    syb_file = CURRENT_DIR+'data/report_data/syb_report' + today + '.csv'
    bd_file = CURRENT_DIR+'data/report_data/bd_report' + today + '.csv'
    syb_file_yes = CURRENT_DIR+'data/report_data/syb_report' + yesterday + '.csv'
    bd_file_yes = CURRENT_DIR+'data/report_data/bd_report' + yesterday + '.csv'
    if not os.path.exists(syb_file) and not os.path.exists(syb_file_yes):
        logger.error('analysis_campaign error: %s not exists ' % (syb_file))
        return None

    syb_file_use = syb_file
    bd_file_use = bd_file
    if not os.path.exists(syb_file) and os.path.exists(syb_file_yes):
        syb_file_use = syb_file_yes
        bd_file_use = bd_file_yes 
    try:
        content = analysis_campaign(syb_file_use, bd_file_use)
        #send_email_with_text(DIRECTOR['EMAIL'], content, today+'_产品报表日常分析')
        send_email_with_text('product@maimiaotech.com', content, today+'_产品报表日常分析')
        send_email_with_text('xuyaoqiang@maimiaotech.com', content, today+'_产品报表日常分析')
        #send_email_with_text('chenke@maimiaotech.com', content, today+'_产品报表日常分析')

    except Exception,e:
        logger.exception('analysis_campaign error: %s' % (str(e)))
        send_sms(DIRECTOR['PHONE'], 'analysis_campaign error: %s' % (str(e)))
    else:
        logger.info('analysis_campaign ok')

if __name__ == '__main__':
    analysis_campaign_script()
    #print analysis_campaign('/home/zhoujiebing/Analysis/DataAnalysis/data/report_data/report2013-04-17.csv')

