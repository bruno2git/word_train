#-*- coding: utf-8 -*-

#>Ideia para um dia em que tenha tempo...
#>> 1) Localização dos dos pares de maior Score <highScoring>.
#>> 2) Expansão dos pares <highScoring> por ambas as extremidades <prefix> e <suffix>, até a um limite <treshold> (score mínimo) formando comboios <LOCAIS>.
#>> 3) Encaixar os combois <LOCAIS> uns nos outros gerar <TRAIN>. Preencher "gaps" com palavras de menor score; em último recurso, remover palavras aos <LOCAIS>.
#>> 4) Usar as restantes palavras nas extremidades do comboio gerado <ou> tentar encaixá-las no interior do combóio mediante critério.
#>> 5) Se o algoritmo usar uma lógica '.pop()' como o actual, no fim, alimentar à função um novo <prefix_dict> com todas as palavras não presentes no <TRAIN>.
#NOTA: Analogia com o algoritmo BLAST.

#> Guiar por palavra mais curta.

#> Inserir critério de paragem mais prático na função maxTrain.
#>> Contador de iterações desdo último maxScore (newBest);
#>> Se o contador chegar a 10000 (p.ex) ou se o Score chegar a (maxScore - 1000) TERMINAR.
#  (valores a avaliar)

#> Criar a opção de maximizar comprimento da cadeia, em vez de Score.
#> Opção 'overwrite (Y/N)?'
#> Questão da terminação em 'suturas': esta é a terminação mais frequente no primeiro 'wordTrain', o que implica que as palavras começadas por 's' já terminaram.
#>> Talvez um critério que desse prioridade à exploração de outras categorias e deixasse a categoria das começadas por 's' para o fim.
#> Estudar a frequência das palavras do dicionário face à primeira letra (fácil) e utilizar isso como parâmetro na escolha do sufixo/prefixo.


'''
#======================================================================================================================================================================#
#Run test functions (at the bottom) for "user interface":                                                                                                              #
#> Run [test_wordTrain()] to create a single Word Train.                                                                                                               #
#> Run [test_maxTrain()] to continuously (iteratively) generate Word Trains, storing the one with max score.                                                           #
#Note1: [maxTrain()] will take a very large amount of time (several hours) to reach max score with a realistic dataset.                                                #
#Note2: [maxTrain()] does not converge at max score but continues to run until all words have been used.                                                               #
#Note3: [maxTrain()] can be interrupted at any moment by the user (whith keyboard interrupt comand (Ctrl+C)) and will return <maxTrain>, <maxScore> and <prefix_dict>. #
#Note4: The Word Train and Prefix:Suffix(es) dictionary returned by [wordTrain] and [maxTrain] can be used as arguments for [maxTrain] to generate new trains.         #
#======================================================================================================================================================================#
'''


#------------------------------------------------------------------------------------------------------------------------------------------#
#>> [wordTrain]                                                                                                                            #
#> Generates a Word Train                                                                                                                  #
#> Inputs: - Train's First Word <startword>; - Name of text file with Words <word_file>; - Separator of Words in file <Sep>.               #
#> Outputs: - List with Word Train <Train>; - Train score <Train_score>; - Dictionary with Prefix:Suffix(es) correspondence <prefix_dict>. #
#  Note1: <startword> must be contained in <word_file>.                                                                                    #
#  Note2: <Train> and <prefix_dict> can be used as arguments for [maxTrain] in order to search for alternative word trains.                #
#------------------------------------------------------------------------------------------------------------------------------------------#
def wordTrain (startword = 'a', word_file = 'dicio.txt', sep = '\n'):
    from time import clock
    Train = []
    Train_score = 0
    prefix_dict = {} # key = prefix; value(s) = suffixe(s)
    try:
        File = open(word_file, 'r')
    except IOError:
        print '<File not found>'
        return None, None, None
    tempword = File.read()
    File.close()
    word_list = tempword.split(sep)
    tempword = None
    try:
        word_list.remove(startword)
    except ValueError:
        print '<Unrecognized word>'
        return None, None, None
    start_time = clock()
    for word in word_list:
        for i in xrange(1, len(word)+1):
            prefix = word[:i]
            rest = word[i:]
            if prefix_dict.has_key(prefix):
                prefix_dict[prefix].append(rest)
            else:
                prefix_dict[prefix] = [rest]
    for prefix in prefix_dict.iterkeys():
        prefix_dict[prefix].sort(reverse=True)
    word = startword
    endStation = False
    while not endStation:
        Train.append(word)
        newStation = False
        i = 0
        while not newStation and i < len(word):
            suffix = word[i:]
            if prefix_dict.has_key(suffix):
                while prefix_dict[suffix] != [] and not newStation:
                    temp_word = suffix + prefix_dict[suffix].pop()
                    if temp_word not in Train:
                        word = temp_word
                        Train_score += len(suffix)**2
                        newStation = True
            i += 1
        if not newStation:
            endStation = True
    stop_time = clock()
    print '<Elapsed time = %s seconds>' % round(stop_time - start_time, 2)
    return Train, Train_score, prefix_dict



#------------------------------------------------------------------------------------------------#
#>> [prefix_dict_generator]                                                                      #
#> Generates a sorted dictionary with Prefix:Suffix(es) correspondence.                          #
#> Inputs: - First word of the Train <startword> (in order not to include it on the dictionary); #
#          - Name of text file with words <word_file>; - separator of words in text file <Sep>.  #
#> Output: - Dictionary with sorted Prefix:Suffix(es) correspondance <prefix_dict>.              #
#  Note1: [prefix_dict_generator] is called by [max_wordTrain].                                  #
#  Note2: <prefix_dict> is use as argument in [alternative_Train] and [maxTrain].                #
#  Note3: Sorts by reverse alphabetical order and word size.                                     #
#------------------------------------------------------------------------------------------------#
def prefix_dict_generator (startword = 'a', word_file = 'dicio.txt', sep = '\n'):
    prefix_dict = {} # key = prefix; value(s) = word(s)
    try:
        File = open(word_file, 'r')
    except IOError:
        print '<File not found>'
        return None
    tempword = File.read()
    File.close()
    word_list = tempword.split(sep)
    tempword = None
    try:
        word_list.remove(startword)
    except ValueError:
        print '<Unrecognized word>'
        return None
    for word in word_list:
        for i in xrange(1, len(word)+1):
            prefix = word[:i]
            rest = word[i:]
            if prefix_dict.has_key(prefix):
                prefix_dict[prefix].append(rest)
            else:
                prefix_dict[prefix] = [rest]
    for prefix in prefix_dict.iterkeys():
        prefix_dict[prefix].sort(reverse=True)
    return prefix_dict



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#>> [alternative_Train]                                                                                                                                                              #
#> Generates a Word Train (alternative to the inputed one)                                                                                                                           #
#> Inputs: - Word from wich to Diverge from iniputed Train <startword>; - previoulsy generated Word Train <Train>; - Dictionary with Prefix:Suffixe(s) correspondence <prefix_dict>. #
#> Outputs: - Word Train alternative to inputed one <Train>; Prefix:Suffixe(s) dictionary <prefix_dict> (altered version of inputed one).                                            #
#  Note1: Alternative Train is generated as long as <startword> is not equal to last word in inputed Train.                                                                          #
#  Note2: While not required, [alternative_Train] will converge faster if inputed <prefix_dict> matches inputed <Train> (as outputs of [wordTrain] or [alternative_Train]);          #
#         Inputing a newly generated <prefix_dict> will only harm performance;                                                                                                       #
#         Inputing a used <prefix_dict> that does not match input <Train> may wrongly limit the alternative train generated.                                                         #
#  Note3: [alternative_Train] is called by [max_wordTrain] and [maxTrain].                                                                                                           #
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def alternative_Train (startword, Train, prefix_dict):
    #Train = []
    #Train_score = 0
    word = startword
    endStation = False
    while not endStation:
        Train.append(word)
        newStation = False
        i = 0
        while not newStation and i < len(word):
            suffix = word[i:]
            if prefix_dict.has_key(suffix) and prefix_dict[suffix] != []:
                while prefix_dict[suffix] != [] and not newStation:
                    temp_word = suffix + prefix_dict[suffix].pop()
                    if temp_word not in Train:
                        word = temp_word
                        #Train_score += len(suffix)**2
                        newStation = True
            i += 1
        if not newStation:
            endStation = True
    return Train, prefix_dict #,Train_score



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#>> [max_wordTrain]                                                                                                                                                        #
#> Continuously (iteratively) generates Word Trains, storing the one with max score.                                                                                       #
#> Inputs: - Train's first Word <startword>; - reference Score <myBest> (only higher scoring Trains are considered),                                                       #
#          - Name of text file with words <word_file>; - separator of words in <word_file> <Sep>.                                                                          #
#> Outputs: - Higher Scoring Train <maxTrain>; - Higher Score <maxScore>; - Prefix:Suffix(es) Dictionary <prefix_dict>.                                                    #
#  Note1: Take's a large amount of time (several hours) to reach max score with a realistic dataset.                                                                       #
#  Note2: Does not converge at max score but continues to run until all words are used (this does not mean a Train with all words but all words spent in multiple Trains). #
#  Note3: Can be interrupted at any moment by the user (whith keyboard interrupt comand (Ctrl+C)) and will return its outputs.                                             #
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def max_wordTrain(startword, myBest = 1191305, word_file = 'dicio.txt', sep = '\n'):
    prefix_dict = prefix_dict_generator(startword, word_file, sep)
    Train = []
    Train, prefix_dict = alternative_Train(startword, Train, prefix_dict)
    Score = trainScore(Train)
    print Score
    maxScore = myBest
    maxTrain = []
    End_of_Line = False
    while not End_of_Line:
        try:
            previous_Train = Train
            previous_score = Score
            w = len(previous_Train)-2 #ignores last word
            Train, prefix_dict = alternative_Train(previous_Train[w], previous_Train[:w], prefix_dict)
            Score = trainScore(Train)
            print Score
            if Score > maxScore:
                maxScore = Score
                maxTrain = Train
                print '------------------------------- new_BEST -------------------------------'
            if w < 0:
                End_of_Line = True
        except:
            return maxTrain, maxScore, prefix_dict
    return maxTrain, maxScore, prefix_dict


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#>> [maxTrain]                                                                                                                                                              #
#> Continuously (iteratively) generates Word Trains, storing the one with max score. -> Can continue from a previously generated Train. <-                                  #
#> Inputs: - Previously generated Word Train <Train>; - Prefix:Suffix(es) dictionary <prefix_dict>.                                                                         #
#> Outputs: - Higher Scoring Train <maxTrain>; - Higher Score <maxScore>; - Prefix:Suffix(es) Dictionary <prefix_dict>.                                                     #  
#  Note1: Take's a large amount of time (several hours) to reach max score with a realistic dataset.                                                                        #
#  Note2: Does not converge at max score but continues to run until all words are used (this does not mean a Train with all words but all words spent in multiple Trains).  #
#  Note3: Can be interrupted at any moment by the user (whith keyboard interrupt comand (Ctrl+C)) and will return its outputs.                                              #
#  Note4: Its outputs can be fed back as arguments to continue the iterative process.                                                                                           #
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def maxTrain(Train, prefix_dict):
    maxScore = trainScore(Train)
    maxTrain = Train
    End_of_Line = False
    while not End_of_Line:
        try:
            previous_Train = Train
            w = len(previous_Train)-2 #ignores last word
            Train, prefix_dict = alternative_Train(previous_Train[w], previous_Train[:w], prefix_dict)
            Score = trainScore(Train)
            print Score
            if Score > maxScore:
                maxScore = Score
                maxTrain = Train
                print '------------------------------- new_BEST -------------------------------'
            if w < 0:
                End_of_Line = True
        except:
            return maxTrain, maxScore, prefix_dict
    return maxTrain, maxScore, prefix_dict



#---------------------------------------------------------------------------------------------------#
#>> [validTrain]                                                                                    #
#> Verifies if there are no repeated words in the word train.                                       #
#> Input: Word Train (list of strings) <Train>.                                                     #
#> Output: Boolean <True> if Train has no repeated words,                                           #
#          Boolean <False> if Train has a repeated word.                                            #
#  Note: This does not prove that <Train> is a valid Word Train;                                    #
#        Obtaining <True> in [validTrain] and a <score> in [trainScore] prove the Train's validity. #
#---------------------------------------------------------------------------------------------------#
def validTrain (Train):
    word_frequence = {}
    for w in Train:
        if word_frequence.has_key(w):
            word_frequence[w] += 1
        else:
            word_frequence[w] = 1
    for k in word_frequence.iterkeys():
        if word_frequence[k] > 1:
            print '<invalid train: %s repeats %s times>' %(k, d[k])
            return False
        else:
            return True
        


#-----------------------------------------------------------------------------------------------------#
#>> [trainScore]                                                                                      #
#> Returns the score of a Word Train.                                                                 #
#> Input: - Word Train <Train>.                                                                       #
#> Output: - Score of Word Train <Train_score> (if Train is valid);                                   #
#          - <None> if Train's not valid (prints '<train crash>').                                    #
#  Note1: Score is calculated as the Total Sum of Squared prefix:suffix number of matched characters. #
#  Note2: Does not check for repeated words; run [validTrain] to that effect.                         #
#-----------------------------------------------------------------------------------------------------#
def trainScore (Train):
    Train_score = 0
    for i in xrange(len(Train)-1):
        word1 = Train[i]
        word2 = Train[i+1]
        match = False
        j = 0
        while not match and j < len(word1):
            suffix = word1[j:]
            size = len(suffix)
            prefix = word2[:size]
            if suffix == prefix:
                match = True
                Train_score += size**2
            j += 1
        if j == len(word1) and not match:
            print '<train crash>'
            return None
    return Train_score



#---------------------------------------------------------------------------------------#
#>> [writeTrain]                                                                        #
#> Writes the Word Train to a Text File, one word per line.                             #
#> Inputs: - Word Train <Train>; - Name of File <file_name>.                            #
#> Output: - Text File named <file_name> with Word Train, one word per line.            #
#  Note1: If there is a file named <file_name> in the directory it will be overwritten. #
#  Note2: The Train can be recovered from the File with [loadTrain].                    #
#---------------------------------------------------------------------------------------#
def writeTrain (Train, file_name = 'myTrain.txt'):
    try:
        File = open(file_name, 'w')
        for word in Train[:len(Train)-1]:
            File.write((word+'\n').encode('utf-8'))
        File.write((Train[len(Train)-1]).encode('utf-8'))
        File.close()
    except:
        print '<error>'
        File.close()



#---------------------------------------------------------------------------------------#
#>> [loadTrain]                                                                         #
#> Loads the Word Train from a Text File to a List with one word per field.             #
#> Inputs: - Name of File with Word Train <file_name>.                                  #
#> Output: - List with one word per field (word train) <Train>;                         #
#          - Empty list if empty file or file not found.                                #
#  Note: The Train can be recorded in a file with [writeTrain].                         #
#---------------------------------------------------------------------------------------#
def loadTrain (file_name = 'myTrain.txt'):
    try:
        File = open(file_name, 'r')
        temp = File.read()
        File.close()
        tTrain = temp.split('\n')
        Train = []
        for w in tTrain:
            Train.append(w.strip())
        return Train
    except IOError:
        print '<file not found>'
        return None



#----------------------------------------------------------------------------------------#
#>> [writePD]                                                                            #
#> Writes the Prefix:Suffix(es) dictionary to a Text File.                               #
#> Inputs: - Prefix:Suffix(es) dictionary <prefix_dict>; - Name of File <file_name>.     #
#> Output: - Text File named <file_name> with Prefix:Suffix(es) dictionary.              #
#  Note1: If there is a file named <file_name> in the directory it will be overwritten.  #
#  Note2: The Prefix:Suffix(es) dictionary can be recovered from the File with [loadPD]. #
#----------------------------------------------------------------------------------------#
def writePD (prefix_dict, file_name = 'prefix_dict.txt'):
    import json
    try:
        File = open(file_name,'w')
        temp = json.dumps(prefix_dict)
        File.write(temp)
        File.close()
    except:
        print '<error>'
        File.close()
    


#---------------------------------------------------------------------------------------#
#>> [loadPD]                                                                            #
#> Loads the Prefix:Suffix(es) dictionary from a Text File to a Dictionary object.      #
#> Inputs: - Name of File with Prefix:Suffix(es) dictionary <file_name>.                #
#> Output: - Dictionary object with Prefix:Suffix(es) correspondence <prefix_dict>;     #
#          - Empty dictionary if empty file or file not found.                          #
#  Note: The Prefix:Suffix(es) dictionary can be recorded to a file with [writePD].     #
#---------------------------------------------------------------------------------------#
def loadPD (file_name = 'prefix_dict.txt'):
    try:
        import json
        File = open(file_name, 'r')
        temp = File.read()
        File.close()
        prefix_dict = json.loads(temp)
        return prefix_dict
    except IOError:
        print '<file not found>'
        return None



#----------------------------------------------------------------------------------------------------#
#>> [indentTrain]                                                                                    #
#> Generates an indented Word Train, aligning prefix of word (i) to suffix of word (i-1).            #
#> Input: Word Train <Train> (list with one word per field).                                         #
#> Output: Indented Word Train <iTrain> (list with one word preceded by necessary spaces per field). #
#  Note: The main purpose of this function is to allow the Word Train to be printed aligned;         #
#        <iTrain> will not be correctly interpreted by any function that receives <Train>.           #
#----------------------------------------------------------------------------------------------------#
def indentTrain (Train):
    iTrain = [Train[0]]
    ilevel = 0 #stores previous indentation 
    for i in xrange(len(Train)-1):
        word1 = Train[i]
        word2 = Train[i+1]
        match = False
        j = 0
        if ilevel >= 90:
                ilevel = 0
        while not match and j < len(word1):
            suffix = word1[j:]
            size = len(suffix)
            prefix = word2[:size]
            if suffix == prefix:
                match = True
                ilevel += len(word1)-len(suffix)
                iTrain.append(ilevel*' ' + word2)
            j += 1
        if j == len(word1) and not match:
            print '<train crash>'
            return None
    return iTrain



#Checks if <filename.ext> exists in directory and replaces it with <filename(z).ext> 
def dont_overwrite (filename):
    from os import path
    z = 1
    while path.exists(filename):
        E = filename.rfind('.')
        Y = filename.rfind(')')
        if Y == E-1:
            X = filename.rfind('(')
            filename = filename[:X] + '(%s)' %str(z) + filename[E:]
        else:
            filename = filename[:E] + '(%s)' %str(z) + filename[E:]            
        z += 1
    return filename



#User interface for <wordTrain> and <maxTrain>.
def test_wordTrain ():
    improve = ''
    print '================== < Word Train > =================='
    while True:
        startAnew = raw_input('[S]tart new word train <or> [C]ontinue from saved train? ').upper()
        if startAnew == 'S' or startAnew == 'C':
            break
    if startAnew == 'S':
        while True:
            startWord = raw_input("Input Train's first word: ").lower()
            T, S, PD = wordTrain(startWord)
            if T != None or S != None or PD != None:
                break
        print '\nWord Train:\n[%s --> %s]\nScore= %s\nLength= %s words\n(%s %% of dictionary)\n'\
        %(T[0], T[len(T)-1], S, len(T), round(len(T)/96045.0*100, 2))
        while True:
            write_to_file = raw_input('Write Train to text file (Y/N)? ').upper()
            if write_to_file == 'Y' or write_to_file == 'N':
                break
        if write_to_file == 'Y':
            while True:
                indent = raw_input('Indent train (Y/N)? ').upper()
                if indent == 'Y' or indent == 'N':
                    break
            if indent == 'Y':
                iT = indentTrain(T)
            else:
                iT = T
            T_filename = startWord.upper() + '_Train.txt'
            T_filename = dont_overwrite(T_filename)
            writeTrain(iT, T_filename)
            PD_filename = startWord.upper() + '_PD.txt'
            PD_filename = dont_overwrite(PD_filename)
            writePD(PD, PD_filename)
        while True:
            improve = raw_input('Search for alternative word trains (Y/N)? ').upper()
            if improve == 'Y' or improve == 'N':
                break
        if improve == 'N':
            while True:
                printTrain = raw_input('Print Train (Y/N)? ').upper()
                if printTrain == 'Y' or printTrain == 'N':
                    break
            if printTrain == 'Y':
                while True:
                    indent = raw_input('Print indented train (Y/N)? ').upper()
                    if indent == 'Y' or indent == 'N':
                        break
                if indent == 'Y':
                    iT = indentTrain(T)
                else:
                    iT = T
                    print '\n-- START --'
                    for w in iT:
                        print w
                    print '--- END ---'
    if startAnew == 'C':
        while True:
            T_filename = raw_input("Input stored Train's file name: ")
            if T_filename[len(T_filename)-4:] != '.txt':
                T_filename = T_filename + '.txt'
            T = loadTrain(T_filename)
            if T != None:
                break
        while True:
            PD_filename = raw_input("Input stored Prefix Dictionary file name: ")
            if PD_filename[len(PD_filename)-4:] != '.txt':
                PD_filename = PD_filename + '.txt'
            PD = loadPD(PD_filename)
            if PD != None:
                break
    if startAnew == 'C' or improve == 'Y':
        raw_input('<Iterative process may take hours to converge. Interrupt at any time with (Ctrl+C)>')
        maxT, maxS, maxPD = maxTrain(T, PD)
        print '\nWord Train:\n[%s --> %s]\nScore= %s\nLength= %s words\n(%s %% of dictionary)\n'\
        %(maxT[0], maxT[len(maxT)-1], maxS, len(maxT), round(len(maxT)/96045.0*100, 2))
        while True:
            write_to_file = raw_input('Write Train to text file (Y/N)? ').upper()
            if write_to_file == 'Y' or write_to_file == 'N':
                break
        if write_to_file == 'Y':
            while True:
                indent = raw_input('Indent train (Y/N)? ').upper()
                if indent == 'Y' or indent == 'N':
                    break
            if indent == 'Y':
                maxiT = indentTrain(maxT)
            else:
                maxiT = maxT
            maxT_filename = 'max_' + maxT[0].upper() + '_Train.txt'
            maxT_filename = dont_overwrite(maxT_filename)
            writeTrain(maxiT, maxT_filename)
            maxPD_filename = 'max_' + maxT[0].upper() + '_PD.txt'
            maxPD_filename = dont_overwrite(maxPD_filename)
            writePD(maxPD, maxPD_filename)
        while True:
            printTrain = raw_input('Print Train (Y/N)? ').upper()
            if printTrain == 'Y' or printTrain == 'N':
                break
        if printTrain == 'Y':
            while True:
                indent = raw_input('Print indented train (Y/N)? ').upper()
                if indent == 'Y' or indent == 'N':
                    break
            if indent == 'Y':
                maxiT = indentTrain(maxT)
            else:
                maxiT = maxT
            print '\n-- START --'
            for w in maxiT:
                print w
            print '--- END ---'



while True:
    try:
        test_wordTrain()
    except KeyboardInterrupt:
        break
