# uncompyle6 version 3.5.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17)
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: readbq.py
import re
from readbq2 import read_bq2

def sidid_value2list(tmp_value):
    if 'Invalid Format' in tmp_value:
        tmp_list = [
         1]
        tmp_list.append('Invalid Format')
        st = tmp_value.index('(')
        en = tmp_value.index(')')
        tmp_list.append(tmp_value[st + 1:en])
        tmp_list.append(tmp_value[en + 1:])
    elif 'Not Supported' in tmp_value:
        tmp_list = [
         2]
        tmp_list.append(tmp_value)
    elif 'Comm Error' in tmp_value:
        tmp_list = [
         2]
        tmp_list.append(tmp_value)
    elif 'Invalid Month' in tmp_value:
        tmp_list = [
         3]
        tmp_list.append(tmp_value)
    elif 'Unexpected Response' in tmp_value:
        tmp_list = [
         4]
        tmp_list.append(tmp_value)
    else:
        tmp_list = [
         0]
        tmp_list.append(tmp_value)
    return tmp_list


def read_bq(filepath):
    with open(filepath, 'r') as (file):
        bq = file.readlines()
    bq_dic = {}
    read_status = 0
    dtc_txt_status = 0
    ecd_status = 0
    for content in bq:
        line = re.sub('\\\\.*? ', '', content)
        line = re.sub('\\\\.*?$', '', line)
        line = line.replace('}{', '')[:-1]
        if read_status == 1:
            if 'status' not in bq_dic['ecus'][cur_ecu]:
                bq_dic['ecus'][cur_ecu]['status'] = 'Success'
            if line[:15] == 'Loaded MDX File':
                bq_dic['ecus'][cur_ecu]['mdx'] = True
            elif line[:3] == '[0x':
                if 'sidid' not in bq_dic['ecus'][cur_ecu]:
                    bq_dic['ecus'][cur_ecu]['sidid'] = {}
                else:
                    tmp_list = sidid_value2list(tmp_value)
                    bq_dic['ecus'][cur_ecu]['sidid'][lastsidid].append(tmp_list)
                tmpindex = line.index(':')
                tmp = [line[9:tmpindex]]
                lastsidid = line[3:7]
                bq_dic['ecus'][cur_ecu]['sidid'][lastsidid] = tmp
                tmp_value = line[tmpindex + 2:]
            elif line == ' ':
                tmp_list = sidid_value2list(tmp_value)
                bq_dic['ecus'][cur_ecu]['sidid'][lastsidid].append(tmp_list)
            else:
                tmp_value += line
        elif read_status == 2:
            if 'status' not in bq_dic['ecus'][cur_ecu]:
                bq_dic['ecus'][cur_ecu]['status'] = 'Success'
            if 'Number of Returned DTCs' in line:
                st_number = line.index(':')
                bq_dic['ecus'][cur_ecu]['dtcs']['numbers'] = int(line[st_number + 2:])
            elif line[:10] == '     DTC #':
                en = line.index('(')
                cur_dtc = line[en - 7:en - 1]
                dtc_txt = line
                dtc_txt_status = 1
            elif dtc_txt_status == 1:
                dtc_txt_status = 0
                st = dtc_txt.index('[')
                en = dtc_txt.index(']')
                dtc_name = dtc_txt[st + 1:en]
                bq_dic['ecus'][cur_ecu]['dtcs'][cur_dtc] = {}
                bq_dic['ecus'][cur_ecu]['dtcs'][cur_dtc]['name'] = dtc_name
                st = line.index(':')
                bq_dic['ecus'][cur_ecu]['dtcs'][cur_dtc]['status'] = line[st + 4:st + 6]
        elif read_status == 8:
            if 'status' not in bq_dic['ecus'][cur_ecu]:
                bq_dic['ecus'][cur_ecu]['status'] = 'Success'
        if ecd_status == 0:
            if line[:10] == 'Attempting':
                st = line.index('DID')
                en = line.index('...')
                cur_ecddid = line[st + 6:en - 1]
                bq_dic['ecus'][cur_ecu]['ecds'][cur_ecddid] = {}
            elif line[:19] == '     DataIdentifier':
                cur_ecddid = line[24:28]
                bq_dic['ecus'][cur_ecu]['ecds'][cur_ecddid] = {}
                st = line.index('byte')
                data_size = line[44:st].replace(' ', '')
                bq_dic['ecus'][cur_ecu]['ecds'][cur_ecddid]['DataSize'] = int(data_size)
            elif line[:15] == '     Data (Hex)':
                bq_dic['ecus'][cur_ecu]['ecds'][cur_ecddid]['Data'] = line[17:]
            elif line[:13] == '          [0x':
                ecd_status = 1
                bq_dic['ecus'][cur_ecu]['ecds'][cur_ecddid]['Discription'] = {}
                st = line.index(']')
                en = line.index(':')
                bq_dic['ecus'][cur_ecu]['ecds'][cur_ecddid]['Discription']['mdx_result_name'] = line[st + 2:en]
                ecd_name_content = line[en + 1:]
                ecd_type = '-'
                if '(' in line:
                    if 'Invalid Format' not in line:
                        st2 = line.index('(')
                        en2 = line.index(')')
                        ecd_type = line[st2 + 1:en2]
                        ecd_name_content = line[en + 1:st2]
                    if 'Invalid Format' in line:
                        st2 = line.index('(')
                        en2 = line.index(')')
                        ecd_name_content = ['Invalid Format', line[st2 + 1:en2]]
                bq_dic['ecus'][cur_ecu]['ecds'][cur_ecddid]['Discription']['mdx_result_name_content'] = ecd_name_content
                bq_dic['ecus'][cur_ecu]['ecds'][cur_ecddid]['Discription']['mdx_result_type'] = ecd_type
        if ecd_status == 1:
            if line[:10] == 'Attempting':
                ecd_status = 0
            elif line == ' ':
                ecd_status = 0
                read_status = 0
            elif line[:10] == '          ':
                st = line.index(':')
                bq_dic['ecus'][cur_ecu]['ecds'][cur_ecddid]['Discription'][line[10:st]] = line[st + 1:]
            else:
                bq_dic['ecus'][cur_ecu]['ecds'][cur_ecddid]['Discription']['addtion_content'] = line
        elif read_status == 0:
            if line == '   Found ECU supporting unknown protocol.':
                # bq_dic['ecus'].pop(cur_ecu)
                bq_dic['ecus'][cur_ecu]['status'] = 'Failure'

        if line[:20] == 'Performing Iteration':
            return read_bq2(filepath)
        if line[:5] == 'Date:':
            bq_dic['date'] = line[6:16]
            st = line.index('Time:')
            if 'M' in line:
                en = line.index('M')
                bq_dic['time'] = line[st + 6:en + 1]
            else:
                en = line.index('(')
                bq_dic['time'] = line[st + 6:en - 2]
            st = line.index('(')
            en = line.index(')')
            bq_dic['version'] = line[st + 1:en]
        elif line[:5] == 'ECU #':
            if 'ecus' not in bq_dic:
                bq_dic['ecus'] = {}
            cur_ecu = line[-5:-2]
            bq_dic['ecus'][cur_ecu] = {}
            bq_dic['ecus'][cur_ecu]['mdx'] = False
            read_status = 0
        elif line[:12] == 'DTC Summary:':
            read_status = 11
        else:
            if read_status >= 0:
                if read_status <= 10:
                    pass
            if line[:40] == 'Requesting Standard Identification DIDs:':
                read_status = 1
            elif line[:49] == 'Requesting to Read DTCs using DTCStatusMask 0x8F:':
                read_status = 2
                bq_dic['ecus'][cur_ecu]['dtcs'] = {}
            elif line[:42] == 'Requesting to Read ECU Configuration DIDs:':
                read_status = 8
                bq_dic['ecus'][cur_ecu]['ecds'] = {}

    return bq_dic


if __name__ == '__main__':
    print(read_bq('BQ NEL00098 O.rtf'))