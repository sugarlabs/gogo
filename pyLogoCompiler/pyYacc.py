# -*- coding: utf-8 -*-
#----------------------------BRGOGO----------------------------------------
#Project site: http://br-gogo.sourceforge.net
#
# Name: pyLogo
# Origiginal from: Marcelo Barbosa
# About: Esta é uma versão da linguagem Logo em python para a placa Gogo board
#
# Modified by: Felipe Augusto Silva
# email: suportegogo@gmail.com
# compiler version: 0.23
#-----------------------------------------------------------------------------

from gettext import gettext as _

from .ply import yacc

#Pega os tokens já checados no analisador léxico
from .pyLex import tokens
from . import pyLex

CODE_START = [0]
CODE_STOP = [7]
Erros = ""
       
#Precedência de operadores na linguagem
precedence = (('left', 'AND', 'OR', 'XOR'),  
              ('left', 'LESSTHAN', 'GREATERTHAN'),  
              ('left', 'PLUS', 'MINUS'),
              ('left', 'TIMES', 'DIVIDE', 'PERCENT'),
              ('right', 'UMINUS'),            # Operador unário MINUS
              ('right', 'UNOT'),              # Operador unário NOT 
              )

globais = { }

#saida = []

src_code = ''
errMsgFunc = None

variaveis = []
vlocais = {}
nvlocais = 0
nomeprocs = { }
size = 0 #tamanho do codigo ja compilado
procname = ''#nome do procedimento sendo compilado

DEBUG = True
RECOMPILE = False

def p_procedures(p):
    '''procedures : procedure procedures'''
    print(" # pyYacc -> p_procedures")
    p[0] = p[1] + p[2]

def p_procedures_procedure(p):
    'procedures : procedure '
    print(" # pyYacc -> p_procedures_procedure p[0]=p[1]='%s'" % p[1])
    p[0] = p[1]

#TODO: remove tmp refs to RECOMPILE...
def p_procedure(p):
    '''procedure : TO PROCEDURENAME statements END'''
    global RECOMPILE
    try:
        l = []
        global size

        print(" # pyYacc -> p_procedure")
        for i in range(4):
            print("p[",i+1,"]", p[i+1])

        procname=p[2]
        nomeprocs[procname]=size
        if p[1] == 'to' and p[4] == 'end':
            l.append(nvlocais) #code_start
            l += p[3]
            l.append(7) #code_end
            p[0] = l
            size += len(l)
        else:
            #raise Exception, _("Nome não determinado '%s'") % p[2]
            raise Exception(_("Name not found '%s'") % p[2])
    except AttributeError:
        #raise Exception, _("Nome não determinado '%s'") % p[2]
        raise Exception(_("Name not found '%s'") % p[2])
        p[0] = 0
        
    RECOMPILE = True

def p_procedure_parametere(p):
    '''procedure : TO PROCEDURENAME parameterDeclaration statements END'''
    try:
        l = []
        print(" # pyYacc -> p_procedure_parametere")
        global size

        procname=p[2]
        nomeprocs[procname]=size
        print('nomeprocs: ',nomeprocs)
        if p[1] == 'to' and p[5] == 'end':
            global nvlocais
            global vlocais
            l.append(nvlocais)
            #global RECOMPILE
            #RECOMPILE=True#para q 'statements' acesse os parametros da funcao
            l += p[4]
            l.append(7) #code_end
            nvlocais=0
            vlocais={}
            p[0] = l
            size += len(l)
        else:
            #raise Exception, _("Nome não determinado '%s'") % p[2]
            raise Exception(_("Name not found '%s'") % p[2])
    except ValueError:
        #print _("Nome não determinado '%s'") % p[2]
        print(_("Name not found '%s'") % p[2])
        p[0] = 0

def p_parameterDeclaration(p):
    '''parameterDeclaration : RECEIVER parameterDeclaration 
                            | RECEIVER'''
    print(" # pyYacc -> p_parameterDeclaration")
    print("p[1] = '%s'" % p[1],len(p))

    try:
        global nvlocais
        x=-1
        while not p[x]=='to':
            x-=1

        procname=p[x+1]
        nvlocais+=1
        print(procname)
        print(vlocais)
        if not procname in vlocais:
            vlocais[procname]=[]
        vlocais[procname].insert(0,p[1])
    except:
        #print _("Nome não determinado '%s'") % p[1]
        print(_("Name not found '%s'") % p[1])
        p[0] = []

def p_statements(p):
    '''statements : statement statements'''
    print(" # pyYacc -> p_statements")
    p[0] = p[1] + p[2]

def p_statements_statement(p):
    'statements : statement'
    print(" # pyYacc -> p_statements_statement")
    p[0] = p[1]

def p_statement_repeat(p):
    '''statement : REPEAT expression LBRACKET statements RBRACKET'''
    #representação do repeat: <expressao> <list> <lengthlist> <expressao> <eol> <repeat> 
    print(" # pyYacc -> p_statement_repeat")
    try:
        l =[]
        l += p[2]
        l.append(3)
        if p[3] == '[' and p[5] == ']':
            l2 = p[4]
            l.append(len(l2)+1)#tamanho da lista
            l += l2
            l.append(4)
            #if DEBUG:
            #  print l;
        l.append(9) #repeat
        p[0] =  l
    except LookupError:
        msgErro(p.lineno, p.lexpos, p[2])
        p[0] = []

def p_statement_loop(p):
    '''statement : LOOP LBRACKET statements RBRACKET'''
    print(" # pyYacc -> p_statement_loop")
    try:
        l =[]
        l.append(3)
        if p[2] == '[' and p[4] == ']':
            l2 = p[3]
            l.append(len(l2)+1)#tamanho da lista
            l += l2
            l.append(4)
            #if DEBUG:
            #  print l;
        l.append(15) #loop
        p[0] =  l
    except SyntaxError:
        msgErro(p.lineno, p.lexpos, p[3])
        p[0] = []

def p_statement_forever(p):
    '''statement : FOREVER LBRACKET statements RBRACKET'''
    print(" # pyYacc -> p_statement_forever")
    try:
        l =[]
        l.append(3)
        if p[2] == '[' and p[4] == ']':
            l2 = p[3]
            l.append(len(l2)+1)#tamanho da lista
            l += l2
            l.append(4)
            #if DEBUG:
            #  print l;
        l.append(15) #loop
        p[0] =  l
    except SyntaxError:
        msgErro(p.lineno, p.lexpos, p[3])
        p[0] = []

def p_statement_if(p):
    '''statement : IF expression LBRACKET statements RBRACKET'''
    #representação do repeat: <expressao> <list> <lengthlist> <expressao> <eol> <if> 
    print(" # pyYacc -> p_statement_if")
    try:
        l =[]
        l += p[2]
        l.append(3)
        if p[3] == '[' and p[5] == ']':
            l2 = p[4]
            print(l2)
            l.append(len(l2)+1)#tamanho da lista
            print(len(l2)+1)
            l += l2
            l.append(4)
            #if DEBUG:
            #  print l;
        l.append(10) #if
        p[0] =  l
    except SyntaxError:
        msgErro(p.lineno, p.lexpos, p[2])
        p[0] = []

def p_statement_ifelse(p):
    '''statement : IFELSE expression LBRACKET statements RBRACKET LBRACKET statements RBRACKET'''
    #representação do repeat: <expressao> <list> <lengthlist> <expressao> <eol> (2x) <ifelse> 
    print(" # pyYacc -> p_statement_ifelse")
    try:
        l =[]
        l += p[2]
        l.append(3)
        if p[3] == '[' and p[5] == ']':
            l2 = p[4]
            l.append(len(l2)+1)#tamanho da lista
            l += l2
            l.append(4)
            #if DEBUG:
            #  print l;
        if p[6] == '[' and p[8] == ']':
            l.append(3)
            l2 = p[7]
            l.append(len(l2)+1)#tamanho da lista
            l += l2
            l.append(4)
            #if DEBUG:
            #  print l;
        l.append(11) #ifelse
        p[0] =  l
    except LookupError:
        msgErro(p.lineno, p.lexpos, p[2])
        p[0] = []

def p_statement_waituntil(p):
    '''statement : WAITUNTIL LBRACKET expression RBRACKET'''
    #representação do repeat: <list> <lengthlist> <expressao> <eolr> <waituntil> 
    print(" # pyYacc -> p_statement_waituntil")
    try:
        l =[]
        if p[2] == '[' and p[4] == ']':
            l.append(3)
            l2 = p[3]
            l.append(len(l2)+1)#tamanho da lista
            l += l2
            l.append(5)
            #if DEBUG:
            #  print l;
        l.append(14) #waituntil
        p[0] =  l
    except LookupError:
        msgErro(p.lineno, p.lexpos, p[3])
        p[0] = []

def p_statement_when(p):
    '''statement : WHEN expression LBRACKET expression RBRACKET'''
    #representação do repeat: <list> <lengthlist> <expressao> <eolr> <waituntil> 
    print(" # pyYacc -> p_statement_when")
    try:
        l =[]
        l += p[2]
        if p[3] == '[' and p[5] == ']':
            l.append(3)
            l2 = p[3]
            l.append(len(l2)+1)#tamanho da lista
            l += l2
            l.append(4) #whenoff
            #if DEBUG:
            #  print l;
        l.append(44)
        p[0] =  l
    except LookupError:
        msgErro(p.lineno, p.lexpos, p[3])
        p[0] = []

#def p_statement_show(p):
    #'''statement : SHOW REPORTER'''
    #print " # pyYacc -> p_statement_SHOW p= '%s'" %p[2]

    #l=[]
    #pos=0

    #for i in variaveis:
        #if i == p[2]:
            #break
        #pos+=1

    #pos-=1

    #if pos == -1: #nenhuma variavel encontrada
        ##raise TypeError, "Nome não determinado '%s'" % p[2]
        #raise Exception, _("Name not found '%s'") % p[2]
        #p[0]=[]

    #else:
        #l.append(91)#CL_I2C_START 

        #l.append(1)
        #l.append(176)
        #l.append(93)#CL_I2C_WRITE
        #l.append(1)
        #l.append(2)
        #l.append(93)#CL_I2C_WRITE

        #l.append(1)
        #l.append(pos)
        #l.append(36)#GETGLOBAL
        #l.append(72)#HIGH_BYTE
        #l.append(93)#CL_I2C_WRITE

        #l.append(1)
        #l.append(pos)
        #l.append(36)#GETGLOBAL
        #l.append(71)#LOW_BYTE
        #l.append(93)#CL_I2C_WRITE

        #l.append(92)#L_I2C_STOP 
        #p[0]=l

def p_statement_show_expression(p):
        '''statement : SHOW expression'''
        print(" # pyYacc -> p_statement_show_expression p= '%s'" %p[2])
        l=[]

        l.append(91)
        l.append(1)
        l.append(176)
        l.append(93)#CL_I2C_WRITE
        l.append(1)
        l.append(2)
        l.append(93)#CL_I2C_WRITE

        print(p[2])
        if len(p[2])==2: #show numbr in display
                if p[2][0]==1:
                        l.append(1)
                        l.append(p[2][1])
                        l.append(72)#HIGH_BYTE
                        l.append(93)#CL_I2C_WRITE
                        l.append(1)
                        l.append(p[2][1])
                        l.append(71)#LOW_BYTE
                        l.append(93)#CL_I2C_WRITE
                if p[2][0]==2:
                        l.append(2)
                        l.append(p[2][1])#hi byte
                        l.append(72)#HIGH_BYTE
                        l.append(93)#CL_I2C_WRITE
                        l.append(2)
                        l.append(p[2][2])#low byte
                        l.append(71)#LOW_BYTE
                        l.append(93)#CL_I2C_WRITE
        else: #show the result of the expression
                l+=p[2]
                l.append(72)
                l.append(93)
                l+=p[2]
                l.append(71)
                l.append(93)
        l.append(92)
        p[0]=l


def p_statement_show_disp(p):
        '''statement : SHOW RECEIVER'''
        print(" # pyYacc -> p_statement_SHOW-disp p= '%s'" %p[2])
        #print _('tamanho'), len(p[2])
        print(_('size'), len(p[2]))
        l=[]

        l.append(91)#CL_I2C_START

        l.append(1)
        l.append(176)
        l.append(93)#CL_I2C_WRITE

        l.append(1)
        l.append(3)
        l.append(93)#CL_I2C_WRITE

        l.append(1)
        l.append(ord(p[2][1]))
        l.append(93)#CL_I2C_WRITE

        l.append(1)
        if (len(p[2]) > 2):
            l.append(ord(p[2][2]))
        else:
            l.append(32)
        l.append(93)#CL_I2C_WRITE

        l.append(1)
        if (len(p[2]) > 3):
            l.append(ord(p[2][3]))
        else:
            l.append(32)
        l.append(93)#CL_I2C_WRITE

        l.append(1)
        if (len(p[2]) > 4):
            l.append(ord(p[2][4]))
        else:
            l.append(32)
        l.append(93)#CL_I2C_WRITE

        l.append(92)#CL_I2C_STOP

        p[0]=l

def p_statement_make(p):
    '''statement : MAKE RECEIVER expression'''
    print(" # pyYacc -> p_statement_MAKE")

    if variaveis.count(p[2])==0:
        pos=len(variaveis)
        variaveis.append(p[2])
    else:
        pos=0
        for i in variaveis:
            if i == p[2]:
                break
            pos+=1

    l=[]
    l.append(1)#NUM8 stkPush(fetchNextOpcode());
    l.append(pos);

    l+=p[3]#add the expression to the list
    l.append(35)#SETGLOBAL
    p[0]=l


def p_statement_expression(p):
    '''statement : WAIT expression
                 | SEND expression
                 | RECORD expression
                 | ERASE expression
                 | SETSVH expression
                 | SVR expression
                 | SVL expression
                 | SETPOWER expression
                 | I2C_WRITE expression
                 | OUTPUT expression
                 | ONFOR expression
                 | BSEND expression
                 | BSR expression
                 | SETDP expression
                 | FASTSEND expression''' 
    print(" # pyYacc -> p_statement_expression")
    try:
        p.lineno(1)
        p.lineno(2)
        l =[]
        l += p[2]
        if p[1] == 'wait':
            op = 16
        elif p[1] == 'send':
            op = 19
        elif p[1] == 'record':
            op = 39
        elif p[1] == 'erase':
            op = 43
        elif p[1] == 'setsvh':
            op = 87
        elif p[1] == 'svr':
            op = 88
        elif p[1] == 'svl':
            op = 89
        elif p[1] == 'setpower':
            op = 59
        elif p[1] == 'i2c_write':
            op = 93
        elif p[1] == 'output':
            op = 8
        elif p[1] == 'onfor':
            op = 50
        elif p[1] == 'bsend':
            op = 61
        elif p[1] == 'bsr':
            op = 62
        elif p[1] == 'setdp':
            op = 42
        elif p[1] == 'fastsend':
            op = 67
        else:
            op = 0
        
        l.append(op)
        p[0] =  l
    except ValueError:
        msgErro(p.lineno, p.lexpos, p[2])
        p[0] = []

def p_statement_value(p):
    '''statement :  BEEP
                  | STOP
                  | RESET
                  | RESETDP
                  | ON
                  | OFF
                  | THISWAY
                  | THATWAY
                  | RD
                  | BRAKE
                  | LEDON
                  | LEDOFF
                  | I2C_START
                  | I2C_STOP
                  | WHENOFF
                  | procedurecall
                  '''
    print(" # pyYacc -> p_statement_value")
    if p[1] == 'beep':
        op = [12]
    elif p[1] == 'stop':
        op = [7]
    elif p[1] == 'reset':
        op = [18]
    elif p[1] == 'resetdp':
        op = [41]
    elif p[1] == 'on':
        op = [49]
    elif p[1] == 'off':
        op = [51]
    elif p[1] == 'thisway':
        op = [52]
    elif p[1] == 'thatway':
        op = [53]
    elif p[1] == 'rd':
        op = [54]
    elif p[1] == 'brake':
        op = [60]
    elif p[1] == 'ledon':
        op = [85]
    elif p[1] == 'ledoff':
        op = [86]
    elif p[1] == 'i2c_start':
        op = [91]
    elif p[1] == 'i2c_stop':
        op = [92]
    elif p[1] == 'whenoff':
        op = [45]       
    else:
        op = p[1]        
    p[0] = op

#def p_statement_motorAttention(p):    
    #'''statement :  MOTORATTENTION'''
    #it works too!!!!
    #print " # pyYacc -> p_statement_motorAttention"
    #if p[1] == 'a,':
        #op = [46]
    #elif p[1] == 'b,':
        #op = [47]
    #elif p[1] == 'ab,':
        #op = [48]
    #elif p[1] == 'c,':
        #op = [63]
    #elif p[1] == 'd,':
        #op = [64]
    #elif p[1] == 'cd,':
        #op = [65]
    #elif p[1] == 'abcd,':
        #op = [66]
    #p[0] = op

def p_statement_motorAttention(p):    
    '''statement :  MOTORATTENTION'''
    print(" # pyYacc -> p_statement_motorAttention")
    l=[]
    l.append(1)
    if p[1] == 'a,':
        l.append(1)
    elif p[1] == 'b,':
        l.append(2)
    elif p[1] == 'ab,':
        l.append(3)
    elif p[1] == 'c,':
        l.append(4)
    elif p[1] == 'ac,':
        l.append(5)
    elif p[1] == 'bc,':
        l.append(6)
    elif p[1] == 'abc,':
        l.append(7)
    elif p[1] == 'd,':
        l.append(8)
    elif p[1] == 'ad,':
        l.append(9)
    elif p[1] == 'bd,':
        l.append(10)
    elif p[1] == 'abd,':
        l.append(11)
    elif p[1] == 'cd,':
        l.append(12)
    elif p[1] == 'acd,':
        l.append(13)
    elif p[1] == 'bcd,':
        l.append(14)
    elif p[1] == 'abcd,':
        l.append(15)
    else:
        raise TypeError("Motor '%s' desconhecido\n Ex.:\n a, on\nab, onfor 3\nbc, setpower 2" % p[1])

    l.append(90)
    p[0] = l

def p_statement_bytes(p):
    '''statement :  BYTES'''
    print(" # pyYacc -> p_statement_bytes")
    if (p[1] == '0x83') or \
       (p[1] == '0x84') or \
       (p[1] == '0x85') or \
       (p[1] == '0x86') or \
       (p[1] == '0x87') :
        op = [1, int((p[1]),16)]
    else:
        op = []
    p[0] = op

def p_expression_reporter(p):
    '''expression : REPORTER'''
    print(" # pyYacc -> p_expression_reporter")

    l=[]
    pos=0
    x=-1
    while not p[x]=='to':
        x-=1

    procname=p[x+1]
    print('procname: ',procname)
    print('vlocais: ',vlocais)
    if (procname in vlocais) and (not vlocais[procname].count('"'+p[1][1:])==0):
            for i in vlocais[procname]:
                if i == '"'+p[1][1:]:
                    break
                pos+=1

            l.append(6)#LTHING(retrieve procedure input)
            l.append(pos)
    else:
        if len(variaveis) == 0:
            #raise TypeError, "Nome não determinado '%s'" % p[1]
            raise TypeError(_("Name not found '%s'") % p[1])

        encontrou=0
        for i in variaveis:
            if i[1:] == p[1][1:]:
                encontrou=1
                break
            pos+=1

        if encontrou == 0: #nenhuma variavel encontrada
            #raise TypeError, "Nome não determinado '%s'" % p[1]
            raise TypeError(_("Name not found '%s'") % p[1])
            p[0]=[]

        else:
            l.append(1)
            l.append(pos)
            l.append(36)#GETGLOBAL

    p[0]=l

def p_expression(p):
    '''expression : expression AND expression
                  | expression OR expression
                  | expression XOR expression
                  | expression LESSTHAN expression
                  | expression GREATERTHAN expression
                  | expression EQUALS expression
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression PERCENT expression'''
    print(" # pyYacc -> p_expression")
    try:
        lexp =[]
        op = 0
        if (len(p) == 4):  #Verifico o tamanho do termo se for 4 então trabalho com os operadores        
            if p[2] == '+':
                op = 23
            elif p[2] == '-':
                op = 24
            elif p[2] == '*':
                op = 25
            elif p[2] == '/':
                op = 26
            elif p[2] == '%':
                op = 27
            elif p[2] == '=':
                op = 28
            elif p[2] == '>':
                op = 29
            elif p[2] == '<':
                op = 30
            elif p[2] == 'and':
                op = 31
            elif p[2] == 'or':
                op = 32
            elif p[2] == 'xor':
                op = 33
        elif (len(p) == 3):
            if p[1] == '-':
                op = 24
            elif p[1] == 'not':
                op = 34

        lexp = []
        lexp += p[1] + p[3]
        lexp.append(op)
        p[0] = lexp
    except TypeError:
        print('Tipos incompativeis! ')
        p[0] = [] 

def p_expression_uminus(p):
    '''expression : MINUS expression %prec UMINUS'''
    print(" # pyYacc -> p_expression_uminus")
    print(p[2])
    lexp = []
    lexp += p[2]
    lexp.append(1)
    lexp.append(0)
    lexp.append(24)    
    p[0] = lexp 

def p_expression_unot(p):
    'expression : NOT expression %prec UNOT'
    print(" # pyYacc -> p_expression_unot")
    lexp = []
    lexp = p[2]
    lexp.append(34)    
    p[0] = lexp  

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    print(" # pyYacc -> p_expression_group")
    try:
        lexp = []
        if p[1] == '(' and p[3] == ')':
            lexp = p[2]
        p[0] =  lexp
    except LookupError:
        msgErro(p.lineno, p.lexpos, p[2])
        p[0] = []

def p_expression_group_bracket(p):
    '''expression : LBRACKET expression RBRACKET'''
    print(" # pyYacc -> p_expression_group_bracket")
    try:
        lexp = []
        if p[1] == '[' and p[3] == ']':
            lexp = p[2]
        p[0] =  lexp
    except LookupError:
        msgErro(p.lineno, p.lexpos, p[2])
        p[0] = []

def p_expression_expression(p):
    '''expression : I2C_READ expression
                  | HIGHBYTE expression
                  | LOWBYTE expression'''
    print(" # pyYacc -> p_expression_group")
    try:
        l =[]
        l += p[2]
        if p[1] == 'i2c_read':
            op = 94
        elif p[1] == 'highbyte':
            op = 72
        elif p[1] == 'lowbyte':
            op = 71        
        else:
            op = 0
            
        l.append(op)                 
        p[0] =  l
    except LookupError:
        msgErro(p.lineno, p.lexpos, p[2])
        p[0] = []
   

def p_expression_value(p):
    '''expression : NUMBERLITERAL
                  | TIMER
                  | RANDOM
                  | RECALL
                  | SENSOR1
                  | SENSOR2
                  | SENSOR3
                  | SENSOR4
                  | SENSOR5
                  | SENSOR6
                  | SENSOR7
                  | SENSOR8
                  | SWITCH1
                  | SWITCH2
                  | SWITCH3
                  | SWITCH4
                  | SWITCH5
                  | SWITCH6
                  | SWITCH7
                  | SWITCH8
                  | NEWIRQ
                  | SERIAL'''
    print(" # pyYacc -> p_expression_value")
    try: 
        p.lineno(1)
        l =[]
        if isinstance(p[1],int):
            print('numero literal')
            if p[1] < 256:
                l.append(1) #é um byte
                l.append(p[1])
            else:
                l.append(2) #é um number
                l.append(highByte(p[1]))
                l.append(lowByte(p[1])) 
        elif p[1] == 'timer':
            l.append(17)
        elif p[1] == 'random':
            l.append(22)
        elif p[1] == 'recall':
            l.append(40)
        elif p[1] == 'sensor1':
            l.append(55)
        elif p[1] == 'sensor2':
            l.append(56)
        elif p[1] == 'sensor3':
            l.append(73)
        elif p[1] == 'sensor4':
            l.append(74)
        elif p[1] == 'sensor5':
            l.append(75)
        elif p[1] == 'sensor6':
            l.append(76)
        elif p[1] == 'sensor7':
            l.append(77)
        elif p[1] == 'sensor8':
            l.append(78)
        elif p[1] == 'switch1':
            l.append(57)
        elif p[1] == 'switch2':
            l.append(58)        
        elif p[1] == 'switch3':
            l.append(79)        
        elif p[1] == 'switch4':
            l.append(80)        
        elif p[1] == 'switch5':
            l.append(81)        
        elif p[1] == 'switch6':
            l.append(82)        
        elif p[1] == 'switch7':
            l.append(83)        
        elif p[1] == 'switch8':
            l.append(84)
        elif p[1] == 'newir?':
            l.append(21)
        elif p[1] == 'serial':
            l.append(82)
        elif p[1] in list(globais.keys()):
            l += globais.get(p[1])
        else:
            #raise SyntaxError, _('Valor não identificado: %s') % p[1]  
            raise SyntaxError(_('Not identified: %s') % p[1])  
            l = p[1]   
        p[0] = l
    except ValueError:
        msgErro(p.lineno, p.lexpos, p[2])
        p[0] = []

def p_parm_value(p):
    '''parm : parm expression
    		| expression'''
    print(" # pyYacc -> p_parm_value %s" % p[1:])
    l=[]
    size=len(p[1:])#get the size of the list 'parm+expression'
    for i in range(1,size+1):
        l+=p[i]#add the last element of the list in parm or the element given
    p[0] = l

def p_procedurecall_parm(p):
    '''procedurecall : PROCEDURENAME parm'''					
    print(" # pyYacc -> p_procedurecall_parm")
    global RECOMPILE
    global errMsgFunc
    
    l=[]
    l.append(128) #SET_PTR_HI_BYTE
    pos=nomeprocs.get(p[1])
    print('jump pos: ','(',pos,')')
    print(nomeprocs)
    if not p[1] in nomeprocs:
        print('**********NEED TO RECOMPILE************')
        if errMsgFunc:
            errMsgFunc(_("Line %(line)d: Unresolved symbol '%(msg)s'") % {'line': p.lineno(1), 'msg': p[1]})
        RECOMPILE=True
    l.append(nomeprocs.get(p[1]))
    p[0]=p[2]+l

def p_procedurecall(p):
    '''procedurecall : PROCEDURENAME'''
    print(" # pyYacc -> p_procedurecall ('%s')" % p[1])
    global RECOMPILE
    global errMsgFunc
    
    l=[]
    l.append(128) #SET_PTR
    pos=nomeprocs.get(p[1])
    print('jump pos: ','(',pos,')')
    if not p[1] in nomeprocs:
        print('**********NEED TO RECOMPILE************')
        if errMsgFunc:
            errMsgFunc(_("Line %(line)d: Unresolved symbol '%(msg)s'") % {'line': p.lineno(1), 'msg': p[1]})
        RECOMPILE=True
    l.append(nomeprocs.get(p[1]))
    p[0]=l

# Compute column. 
#     input is the input text string
#     token is a token instance
def find_column(token):
    global src_code
    last_cr = src_code.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column

def p_error(p):
    global errMsgFunc

    print("# pyYacc -> p_error ('%s')" % p)
    if not (p == None):
        m = msgErro(p.lineno, p.lexpos, p.value)
        # Column calc near impossible for proportional text (esp with tabs)
        #raise SyntaxError, msgErro(p.lineno, find_column(p), p.value)
        #self.showError(msgErro(p.lineno, p.lexpos, p.value))
        #raise SyntaxError, m
        return
    #raise SyntaxError, _("Erro na última linha")
    m = _("Error in last line")
    if errMsgFunc:
        errMsgFunc(m)
    raise SyntaxError(m)

def highByte(number):
    return ((number >> 8) & 0xff)

def lowByte(number):
    return (number & 0xff)

def msgErro(numLine, numPos, value, errMsg=_("Line %(line)d: Syntax Error '%(msg)s'")):
    global errMsgFunc

    #return _("[Linha %d - Coluna %d] - Erro de sintaxe '%s'") % (numLine, numPos, value)
    #return _("[Line %d - Column %d] - Syntax Error '%s'") % (numLine, numPos, value)
    # DMOC: Logo text is in proportional font so getting column is near impossible!
    #TODO: Display chunk of text with error highlighted
    m = errMsg % {'line': numLine, 'msg': value}
    if errMsgFunc:
        errMsgFunc(m)
    return m

def codigoIntermediario(list):
    #print _("Codigo intermediario: %s") % list
    print(_("Intermediate Code: %s") % list)

def codigoFinal(list):
    s=""
    for i in list:
        s = s + chr(i)
    
    #print _("Código Final: %s") % s
    print(_("Final Code: %s") % s)
    return s

#def analisarCodigo(codigo):
    #print " # pyYacc -> analisarCodigo"
    #try:
        ##limpa lista de variaveis
        #del variaveis[:]
        #global RECOMPILE
        #global size
        #global nomeprocs
        #size=0
        #nomeprocs={}
        ##Para usar os analisadores juntos é necessário passar o léxico para dentro do parser.
        #Lexer = pyLex.build()
        #print "    pyLex.build() terminou"
        #parser = yacc.yacc()
        #print "    yacc.yacc() terminou"
        #result = parser.parse(codigo.lower(), lexer=Lexer, tracking=True)
        #if RECOMPILE:
            #print 'RECOMPILE'
            #size=0
            #result = parser.parse(codigo.lower(), lexer=Lexer, tracking=True)
            #RECOMPILE=False
        #print "    parse.parse() gerou resultado '%s'" % result
    #except KeyError, value:
        #return "Erro ao pressionar a tecla: %s" % value
    #except (AttributeError, TypeError, SyntaxError), value:
        #msg = "Os seguintes erros foram detectados: %s" % value + "\n" 
        #return msg
    #else:
        #print 'var locais: ',vlocais,nvlocais
        #return result


def analisarCodigo(codigo, errMsgFunction=None):
    print(" # pyYacc -> analisarCodigo")
    #limpa lista de variaveis
    del variaveis[:]
    
    global RECOMPILE
    global size
    global nomeprocs
    
    global src_code
    global errMsgFunc
    
    errMsgFunc = errMsgFunction
     
    src_code = codigo
    print(src_code)
    
    size=0
    nomeprocs={}
    #Para usar os analisadores juntos é necessário passar o léxico para dentro do parser.
    Lexer = pyLex.build(optimize=1, debug=0)
    print("    pyLex.build() ended")
    parser = yacc.yacc(optimize=1, debug=0)
    print("    yacc.yacc() ended")
    
    pyLex.setErrMsgFunc(errMsgFunc)
    
    if errMsgFunc:
        errMsgFunc('***BEGIN***')
    result = parser.parse(src_code.lower(), lexer=Lexer, debug=0, tracking=True)
    if RECOMPILE:
        print('RECOMPILE')
        size=0
        if errMsgFunc:
            errMsgFunc('***BEGIN***')
        result = parser.parse(src_code.lower(), lexer=Lexer, debug=0, tracking=True)
        #RECOMPILE=False
    if errMsgFunc:
        errMsgFunc('***END***')
    
    print("    parse.parse() generated result '%s'" % result)
    return result
