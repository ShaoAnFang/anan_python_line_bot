
def sticker(key):
    sitckerDict = dict()
    sitckerDict = {'聽歌': {'sticker_id':'103','package_id':'1'}, '想睡': {'sticker_id':'1','package_id':'1'}, 
                    '生日快樂': {'sticker_id':'427','package_id':'1'}, ' 飽': {'sticker_id':'425','package_id':'1'},
                    '騎車': {'sticker_id':'430','package_id':'1'}, '窮': {'sticker_id':'417','package_id':'1'},
                    '很忙': {'sticker_id':'411','package_id':'1'}, '翻滾': {'sticker_id':'423','package_id':'1'},
                    '冷': {'sticker_id':'29','package_id':'2'}, '喝': {'sticker_id':'28','package_id':'2'},
                    '晚安': {'sticker_id':'46','package_id':'2'}, '考試': {'sticker_id':'30','package_id':'2'},
                    '熱': {'sticker_id':'601','package_id':'4'}, '戒指': {'sticker_id':'277','package_id':'4'},
                    '鑽': {'sticker_id':'276','package_id':'4'}, '彩虹': {'sticker_id':'268','package_id':'4'}, 
                    '櫻': {'sticker_id':'604','package_id':'4'}, '累': {'sticker_id':'526','package_id':'2'}, 
                    '生氣': {'sticker_id':'527','package_id':'2'}, '上班': {'sticker_id':'161','package_id':'2'}, 
                    '歡迎': {'sticker_id':'247','package_id':'3'}, '升天': {'sticker_id':'108','package_id':'1'}, 
                    '喇叭': {'sticker_id':'414','package_id':'1'}, '下雨': {'sticker_id':'507','package_id':'2'}}
    # if key in sitckerDict.keys():
    #     return sitckerDict[key]
    # else:
    #     return 'GG'
    lamb = lambda key: sitckerDict[key] if key in sitckerDict.keys() else 'GG'

    return lamb(key)
