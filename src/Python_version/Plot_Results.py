#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
@author: omari
"""
import os
import numpy as np
import cv2
import csv
from QSR_functions import *
import copy
import colorsys

#-------------------------------------------------------------------------------------#
if __name__ == '__main__':

    #-------------- File Path -------------------#
    activity_list = ['arranging_objects/', 'cleaning_objects/', 'having_meal/', 'making_cereal/', 'microwaving_food/', 'taking_food/', 'taking_medicine/']#, 'unstacking_objects/']

    person_id_list = {}
    person_id_list['1'] = {}
    person_id_list['1']['arranging_objects/'] = ['0510175431','0510175554','0510175411']
    person_id_list['1']['cleaning_objects/'] = ['0510181236','0510181310','0510181415']
    person_id_list['1']['having_meal/'] = ['0510182019','0510182057','0510182137']
    person_id_list['1']['making_cereal/'] = ['1204142055','1204142227','1204142500','1204142616']
    person_id_list['1']['microwaving_food/'] = ['1204150645','1204150828','1204151136']
    person_id_list['1']['stacking_objects/'] = ['1204144410','1204144736','1204145234']
    person_id_list['1']['taking_food/'] = ['0510180218','0510180342','0510180532']
    person_id_list['1']['taking_medicine/'] = ['1204142858','1204143959','1204144120']
    #person_id_list['1']['unstacking_objects/'] = ['1204145527','1204145630','1204145902']

    person_id_list['3'] = {}
    person_id_list['3']['arranging_objects/'] = ['0510143426','0510143446','0510143618']
    person_id_list['3']['cleaning_objects/'] = ['0510144324','0510144350','0510144450']
    person_id_list['3']['having_meal/'] = ['0510142336','0510142419','0510142800']
    person_id_list['3']['making_cereal/'] = ['1204173536','1204173846','1204174024','1204174314']
    person_id_list['3']['microwaving_food/'] = ['1204180344','1204180515','1204180612']
    person_id_list['3']['stacking_objects/'] = ['1204175103','1204175316','1204175451']
    person_id_list['3']['taking_food/'] = ['0510144057','0510144139','0510144215']
    person_id_list['3']['taking_medicine/'] = ['1204174554','1204174740','1204174844']
    #person_id_list['3']['unstacking_objects/'] = ['1204175622','1204175712','1204175902']

    person_id_list['4'] = {}
    person_id_list['4']['arranging_objects/'] = ['0510173051','0510173203','0510173217']
    person_id_list['4']['cleaning_objects/'] = ['0510172333','0510172425','0510172557']
    person_id_list['4']['having_meal/'] = ['0510173506','0510173634','0510173714']
    person_id_list['4']['making_cereal/'] = ['1130144242','1130144557','1130144713','1130144814']
    person_id_list['4']['microwaving_food/'] = ['0204140840','0204141007','0204141211']
    person_id_list['4']['stacking_objects/'] = ['1130150747','1130151025','1130151121']
    person_id_list['4']['taking_food/'] = ['0510171810','0510172015','0510172049']
    person_id_list['4']['taking_medicine/'] = ['1130145737','1130145835','1130150135']
    #person_id_list['4']['unstacking_objects/'] = ['1130151154','1130151500','1130151710']

    person_id_list['5'] = {}
    person_id_list['5']['arranging_objects/'] = ['0504235245','0504235647','0504235908']
    person_id_list['5']['cleaning_objects/'] = ['0511140410','0511140450','0511140553']
    person_id_list['5']['having_meal/'] = ['0511141007','0511141231','0511141338']
    person_id_list['5']['making_cereal/'] = ['0126141638','0126141850','0126142037','0126142253']
    person_id_list['5']['microwaving_food/'] = ['0129114054','0129114153','0129114356']
    person_id_list['5']['stacking_objects/'] = ['0129111131','0129112015','0129112226']
    person_id_list['5']['taking_food/'] = ['0505002750','0505002942','0505003237']
    person_id_list['5']['taking_medicine/'] = ['0126143115','0126143251','0126143431']
    #person_id_list['5']['unstacking_objects/'] = ['1130151154','1130151500','1130151710']


    results = []
    for person in ['1','3','4','5']:
        for s in range(3):
            RE = {}
            GT = {}
            f_Stream1 = open('/home/omari/Python/cad120/src/results/stream'+person+'_'+str(s)+'.txt', 'r')
            f_Stream2 = open('/home/omari/Python/cad120/src/results/results_stream'+person+'_'+str(s)+'.txt', 'w')
            for count,line in enumerate(f_Stream1):
                line = line.split('\n')[0]
                if count < 8 and count > 0:
                    data = line.split(':')[1].split(',')
                    GT[line.split(':')[0]] = [int(data[0]),int(data[1])]
                if count > 8:
                    data = line.split(':')[1].split(',')
                    RE[line.split(':')[0]] = [int(data[0]),int(data[1])]
            for key in GT:
                L1 = GT[key][1]-GT[key][0]
                L2 = RE[key][1]-RE[key][0]
                results.append(float(L2)/float(L1))
            f_Stream1.close()
            f_Stream2.close()
    print np.sum(results)/len(results)

    print RE
    print GT
    f = 0
    for key in GT:
        if GT[key][1]>f:
            f=GT[key][1]
    img = np.zeros((200,f,3),dtype=np.uint8)+255

    N = 7
    HSV_tuples = [(x*1.0/N, 1.0, 0.9) for x in range(N)]
    RGB = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    # print RGB_tuples

    colors = {}
    for t,key in enumerate(GT):
        colors[key] = [int(RGB[t][0]*255), int(RGB[t][1]*255), int(RGB[t][2]*255)]

    for key in GT:
        img[0:95,GT[key][0]:GT[key][1],:] = colors[key]

    for key in RE:
        img[105:200,RE[key][0]:RE[key][1],:] = colors[key]

    cv2.imshow('results',img)
    cv2.imwrite('/home/omari/Python/cad120/src/results/results.png',img)
    cv2.waitKey(1000)
