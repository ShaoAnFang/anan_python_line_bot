import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

f = {
      "type": "service_account",
      "project_id": "groupalbum-166505",
      "private_key_id": "7e1b6365be1d48cec5716c208abbf7a7ce0f5095",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDDhNbntwtEgks5\nL5LXIaNwVjyt76L5P5YaG5eQSkoXpNHXuLoPf73yNuT1s7kTArf7sgPwaPess2+K\nDzKPnLc9Bkq728TC5D0lL4hzEKsDe/PdBqLfvoakNySEpJxXziFh/XjlND+BtkXD\nJe15xmuLc9bLZa6uQBWJdzTIoewSStfPMOoghAwLBYDAmlMzuzkK+690SiBUisb0\nOU6Sw96wsX86MO6wKIKBvgMTuegt0I6zVTei1LMsyjQplmFMuF0AUjfuQwo0BS0r\n3Kd0zdZs8OBBTitqfujKpaEVVVm4F6jopWsDqEJkT6LaaRfXRrPZ7p1Mxuv3c3TU\nSBeHzZwhAgMBAAECggEALGm1g4dB6PsL6V6UJYg/nxoHyJ8Bz0qRZzbTU/R8JijL\nfgw5P6IN3MJ5ehKsPNRGRMdoO6ksca+E68COBK9dtGAEg+3lITxFY3gLr8+eeTkj\n6RZD0z1tSko4YmUeGpf5X0/7sV0P/AASksS/0ASxk0jqBuP/LRfjjIlmlRirDnBJ\n46tv5de9XZlH1Twy0fG6+yFJGWd4uLQQm++O8xJ5loyDu7ZdWSYcJ9Bta4Ur41fb\n96tEvk7PnQ9dvGWLs00qIuSSZOigEIk5AuCxeKaMeR3SmdsK7jPuKQ5ZX3i/qcub\n6TIeVvtiZMLcAP5u+aFkTUVOKdE1dY1MEY3xbO/SXQKBgQDyZH28y+7udVwbl6mD\nbaBiqvQFKzHBVhE+x/dyx3Frm5r8ok30MKy375SdNligiGcSbLoLOIg5UJ31BTjf\nWb9f8WblQiHtpixMBbk5PghOwXulq95IOmYDsYR7Hx15KtsVPODBCO4w56RMgFAd\nK2KQa2Cg1nqr4fCCTLKd/AKdHwKBgQDOfrXvl1grKe77Fbb61KkaWqj+/9jCl2vo\nOxyl344BgEDBoXaW+YRmv4y4HXowritVP57URlT46Gq5V6gezGL6elTv6AGXYkRd\nFJGm+QUIj6WFSiQXGVlbdb1RIJrWysb1tb3T77nbAcN8Hgp3U2A+n/dSnO5sTLLG\nzV2sZbdevwKBgQDjoL131CfQZgQWoWl+VC//GL3KMNMr1dCiHZXigyufO2TkBOOi\nAyfgICx3Kvc14oKxCcv5B6Dd+jgsRjgvf4+54PCZMW69R4Vn6yQTfo68rvSYE3vO\nZpEwvL9GBGVgSX+uRRpoDSPqZ06izQjvK7QHHd+Di4dt7OM46h//Pw+RTwKBgBc8\nvR6UKnDZDDKnM+swKUN09lWT1wG25obAuC2WZbWXiDICCIVe2N5zKdPCRXDa+Ldk\nLGx46bEE/pWS3rFwkKbdQ1eoBR3TChxrZySiG0XmXFsOh9ctnBelvUM25xXKxe76\nn70M2h5iKWx7OPRKpqcFe2CJlm8LhobGr4bp/2OjAoGAZjANDFWt8sz1x4hqzdvj\nkKUGGlo66E00II8N1dN5oOfs7mlGBgX9X8uNqCQkewA5yx4lq1YkjiNrucsk8et0\n0lhVXm2k3Bae57gKoGOJ1iSlZpnLQD9sOJCavm39crCRrVtSsiy6vIsc+B3YV+jX\nNIuqgLPiszH2b+00HQMmLi0=\n-----END PRIVATE KEY-----\n",
      "client_email": "testsheet@groupalbum-166505.iam.gserviceaccount.com",
      "client_id": "117086094069483849270",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://accounts.google.com/o/oauth2/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/testsheet%40groupalbum-166505.iam.gserviceaccount.com"
}

#@app.route('/wine', methods=['GET'])
def wine():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(f, scope)
    client = gspread.authorize(creds)
    
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("酒吧巡迴清單").sheet1
    # Extract and print all of the values
    #list_of_hashes = sheet.get_all_records()
    list_of_hashes = sheet.get_all_values()

    notYet = list()
    did = list()
    totalCount = ''
    notYetCount = ''
    didCount = ''
    for sh in range(sheet.row_count):
        #row需要 + 4
        sh = sh + 4
        #print(list_of_hashes[sh])
        if list_of_hashes[sh][2] == '':
            #店名是空就跳出
            #print(int(list_of_hashes[sh][0]) -1)
            totalCount = str(int(list_of_hashes[sh][0]) -1)
            break 
        elif list_of_hashes[sh][1] == '':
            #還沒去過
            notYet.append(list_of_hashes[sh][2] + '\n' + list_of_hashes[sh][3] + '\n' + list_of_hashes[sh][5])
        else:
            #已到訪
            did.append(list_of_hashes[sh][2] + '\n' + list_of_hashes[sh][3] + '\n' + list_of_hashes[sh][5])

    #print(notYet)
    notYetCount = str(len(notYet))
    # print(notYetCount)
    # print(random.choice(notYet))
    didCount = str(len(did))
    print(didCount)
    print(did)

    return random.choice(notYet)


def birthday(date):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(f, scope)
    client = gspread.authorize(creds)

    sheet = client.open("TestList").sheet1
    list_of_hashes = sheet.get_all_values()
    dictionary = dict()

    for sh in range(sheet.row_count):
        #row需要 + 4, 前四row沒資料
        sh = sh + 4
        #print(list_of_hashes[sh])
        if list_of_hashes[sh][1] != '':
            #生日 = list_of_hashes[sh][3]
            #名字 = list_of_hashes[sh][1]
            if list_of_hashes[sh][3] != '':
                #有填生日
                if list_of_hashes[sh][3] in dictionary:
                    names = list()
                    names = dictionary[list_of_hashes[sh][3]]
                    names.append(list_of_hashes[sh][1])
                    dictionary[list_of_hashes[sh][3]] = names
                else:
                    name = list()
                    name.append(list_of_hashes[sh][1])
                    dictionary[list_of_hashes[sh][3]] = name
            else:
                #沒填生日
                if '沒填生日' in dictionary:
                    names = list()
                    names = dictionary['沒填生日']
                    names.append(list_of_hashes[sh][1])
                    dictionary['沒填生日'] = names
                else:
                    name = list()
                    name.append(list_of_hashes[sh][1])
                    dictionary['沒填生日'] = name
        else:
            #名字欄位為空則跳出
            break

    #print(dictionary)
    if date != '沒填生日':
        da = str(date)
        d = da[0] + da[1] + '/' + da[2] + da[3]
        if d in dictionary:
            memberStr = ''
            for m in dictionary[d]:
                memberStr += m + ','
            return memberStr
        else:
            return '沒資料'

    else:

        if date in dictionary:
            memberStr = ''
            for m in dictionary[date]:
                memberStr += m + ','
            return memberStr
        else:
            return '沒資料'