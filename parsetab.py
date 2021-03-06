
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'starterAND CHAR CLOSE COMMENT DIGIT IF IFF NAMEQUOTE NOT NUMERAL OPEN OR QUOTEDSTRING RESERVEDELEMENT STRINGQUOTE\n\t\tstarter : sentence\n\t\t\t\t| sentence starter\n\t\t\n\t\tsentence : atomsent\n\t\t\n\t\tsentence : boolsent\n\t\t\n\t\tmultisent : sentence\n\t\t\t\t  | sentence multisent\n\t\t\t\t  | empty\n\t\t\n\t\tatomsent : OPEN predicate termseq CLOSE\n\t\t\n\t\tpredicate : interpretedname\n\t\t\n\t\ttermseq : interpretedname\n\t\t\t\t| interpretedname termseq\n\t\t\t\t| empty\n\t\t\n\t\tinterpretedname : NUMERAL\n\t\t\t\t\t\t| QUOTEDSTRING\n\t\t\n\t\tboolsent : OPEN AND multisent CLOSE\n\t\t\n\t\tboolsent : OPEN OR multisent CLOSE\n\t\t\n\t\tboolsent : OPEN IF sentence sentence CLOSE\n\t\t\t\t | OPEN IFF sentence sentence CLOSE\n\t\t\n\t\tboolsent : OPEN NOT sentence CLOSE\n\t\tempty :'
    
_lr_action_items = {'OPEN':([0,2,3,4,8,9,10,11,12,20,23,24,26,28,30,33,34,35,],[5,5,-3,-4,5,5,5,5,5,5,5,5,-8,-15,-16,-19,-17,-18,]),'$end':([1,2,3,4,6,26,28,30,33,34,35,],[0,-1,-3,-4,-2,-8,-15,-16,-19,-17,-18,]),'CLOSE':([3,4,7,8,9,13,14,15,16,17,18,19,20,21,22,25,26,27,28,29,30,31,32,33,34,35,],[-3,-4,-20,-20,-20,-9,-13,-14,26,-10,-12,28,-5,-7,30,33,-8,-11,-15,-6,-16,34,35,-19,-17,-18,]),'AND':([5,],[8,]),'OR':([5,],[9,]),'IF':([5,],[10,]),'IFF':([5,],[11,]),'NOT':([5,],[12,]),'NUMERAL':([5,7,13,14,15,17,],[14,14,-9,-13,-14,14,]),'QUOTEDSTRING':([5,7,13,14,15,17,],[15,15,-9,-13,-14,15,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'starter':([0,2,],[1,6,]),'sentence':([0,2,8,9,10,11,12,20,23,24,],[2,2,20,20,23,24,25,20,31,32,]),'atomsent':([0,2,8,9,10,11,12,20,23,24,],[3,3,3,3,3,3,3,3,3,3,]),'boolsent':([0,2,8,9,10,11,12,20,23,24,],[4,4,4,4,4,4,4,4,4,4,]),'predicate':([5,],[7,]),'interpretedname':([5,7,17,],[13,17,17,]),'termseq':([7,17,],[16,27,]),'empty':([7,8,9,17,20,],[18,21,21,18,21,]),'multisent':([8,9,20,],[19,22,29,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> starter","S'",1,None,None,None),
  ('starter -> sentence','starter',1,'p_starter','main.py',170),
  ('starter -> sentence starter','starter',2,'p_starter','main.py',171),
  ('sentence -> atomsent','sentence',1,'p_sentence_atom','main.py',177),
  ('sentence -> boolsent','sentence',1,'p_sentence_bool','main.py',189),
  ('multisent -> sentence','multisent',1,'p_multisent','main.py',202),
  ('multisent -> sentence multisent','multisent',2,'p_multisent','main.py',203),
  ('multisent -> empty','multisent',1,'p_multisent','main.py',204),
  ('atomsent -> OPEN predicate termseq CLOSE','atomsent',4,'p_atomsent','main.py',218),
  ('predicate -> interpretedname','predicate',1,'p_predicate','main.py',229),
  ('termseq -> interpretedname','termseq',1,'p_termseq','main.py',235),
  ('termseq -> interpretedname termseq','termseq',2,'p_termseq','main.py',236),
  ('termseq -> empty','termseq',1,'p_termseq','main.py',237),
  ('interpretedname -> NUMERAL','interpretedname',1,'p_interpretedname','main.py',252),
  ('interpretedname -> QUOTEDSTRING','interpretedname',1,'p_interpretedname','main.py',253),
  ('boolsent -> OPEN AND multisent CLOSE','boolsent',4,'p_boolsent_and','main.py',261),
  ('boolsent -> OPEN OR multisent CLOSE','boolsent',4,'p_boolsent_or','main.py',268),
  ('boolsent -> OPEN IF sentence sentence CLOSE','boolsent',5,'p_boolsent_if','main.py',276),
  ('boolsent -> OPEN IFF sentence sentence CLOSE','boolsent',5,'p_boolsent_if','main.py',277),
  ('boolsent -> OPEN NOT sentence CLOSE','boolsent',4,'p_boolsent_not','main.py',285),
  ('empty -> <empty>','empty',0,'p_empty','main.py',292),
]
