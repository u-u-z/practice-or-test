#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Please use Python3 run it.
'''
写一个程序 go_score_group(cards)，
    cards是一组卡牌 格式是list 
    每一个是一个两个元素的字符 比如 '3H' 就是红桃三 
    程序需要返回一个整数得分 
    
    基于以下： 
        
        每张牌的得分就是它本身的数值 0，J，Q，K，A分别是10，11，12，13，20； 
        
        如果卡组是一套合理的‘N of a kind’(帘)， 
            即两张或以上相同非A数值， 那么得分就是它的数值乘以N的阶乘，
            如go_score_group(['4C', '4H', '4S']) 返回值为24；
        
        如果卡组是一套合理的‘run’（顺子）， 
            即一套三张或以上牌数，最大值和最小值不能为A， 
            根据数值形成一套连续的颜色不同（红黑红或黑红黑）的排序， 
            其中， A可以做为顺子中的任意值， 但颜色固定， 
            得分是每张牌所代表的值的和， 
            A的值取决于它所代表的那张牌的值， 
            这里参数cards的顺序不影响顺子的结果（['2C', '3D', '4S'] 和 ['4S', '2C', '3D']都是顺子）， 
            如
                go_score_group(['2C', 'AD', 'AS','5D']) 返回值9， 
                go_score_group(['2C', '3D', '4H']) 返回值-9； 
                
        如果这要卡组是单张牌或不符合帘和顺子的规则， 
            那么得分即为每张牌数值和的相反数， 
            A在这里值为20， 
            如go_score_group(['4H', '0H', 'JC', '2H', '7H']) 返回值-34


問題分析：
    橋牌基本花色
        C 梅花️ - 黑色
        S 黑桃 - 黑色
        D 方片 - 紅色
        H 紅桃 - 紅色

'''


def get_card_color(card):
    # 1 - 紅
    # 0 - 黑
    if card[1] == 'C' or card[1] == 'c':
        return 0
    elif card[1] == 'S' or card[1] == 's':
        return 0
    elif card[1] == 'D' or card[1] == 'd':
        return 1
    elif card[1] == 'H' or card[1] == 'h':
        return 1
    else:
        return 0


def get_card_score(card):
    if card[0] == '0':
        return 10
    elif card[0] == 'J' or card[0] == 'j':
        return 11
    elif card[0] == 'Q' or card[0] == 'q':
        return 12
    elif card[0] == 'K' or card[0] == 'k':
        return 13
    elif card[0] == 'A' or card[0] == 'a':
        return 20
    else:
        return int(card[0])


def is_nofkind_and_get_score(cards_dict):
    if len(cards_dict) < 2:
        return 0

    n_tmp = cards_dict[0]['card_score']

    for card in cards_dict:
        if card['card_score'] == n_tmp:
            continue
        else:
            return 0

    factorial = 1
    for i in range(1, len(cards_dict) + 1):
        factorial = factorial*i

    return factorial * n_tmp


def is_run_and_get_get_score(cards_dict):
    i = 0
    a_left_score  = 0 
    a_right_score = 0
    
    for card in cards_dict:
        if card['card_score'] == 20:
        # 在有 A 的情況下，強行將A替換成 無A狀態
            if i == 0 or i == (len(cards_dict) - 1 ):
                return 0
            else: 
                a_left_score = cards_dict[i-1]['card_score']
                a_right_score = cards_dict[i+1]['card_score']

                if (a_right_score - a_left_score) == 2:
                    cards_dict[i]['card_score'] = a_left_score + 1
                elif a_right_score == 20:
                    # A 的 下一個 也是 A 的情況下
                    cards_dict[i]['card_score'] = a_left_score + 1
                    cards_dict[i+1]['card_score'] = a_left_score + 2
                else:
                    return 0
        i = i + 1
    
    # 在沒有 A 的情況下
    score = 0
    n_tmp = cards_dict[0]['card_color']
    i = 0

    for card in cards_dict:
        if i == 0:
            i = i + 1
            continue
        elif card['card_color'] != n_tmp:
            n_tmp = card['card_color']
            continue
        else:
            return 0

    new_cards_dict = sorted(cards_dict, key=lambda x: x['card_score'])

    i = 0
    m_tmp = new_cards_dict[0]['card_score']
    for card in new_cards_dict:
        score = score + card['card_score']
        if i == 0:
            i = i + 1
            continue
        else:
            i = i + 1
            if (card['card_score'] - m_tmp) == 1:
                m_tmp = card['card_score']
                continue
            else:
                return 0

    return score


def go_score_group(cards):
    score = 0
    cards_dict = []

    for card in cards:
        cards_dict.append({
            'card_str': card,
            'card_color': get_card_color(card),
            'card_score': get_card_score(card)
        })
        score = get_card_score(card) + score
    run_score = is_run_and_get_get_score(cards_dict)
    kind_score = is_nofkind_and_get_score(cards_dict)
    if run_score > 0 :
        return run_score
    elif kind_score > 0:
        return kind_score
    else:
        return -1 * score


def main():
    print(go_score_group(['4C', '4H', '4S']))
    return 0


if __name__ == "__main__":
    main()
