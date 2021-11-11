class Gramma():
    data = []  # dane (skrypt) z textarea
    error_list = ['Niepoprawna lewa strona produkcji',  # komunikaty błędów
                  'Niewłaściwa ilość symbolu ->',
                  'Brak symbolu . na końcu linii',
                  'Niepoprawny symbol terminalny',
                  'Przekroczono maksymalną liczbę symboli nieterminalnych.',
                  'Lewa strona pierwszej reguły produkcji powinna zawierać jedynie symbol startowy.'
                  ]
    rules = []  # tablica reguł
    str_rules = []  # tablica regul zwyklych
    recursions = []  # tablica reguł rekurencyjnych
    nonTerm = []  # symbole nieterminalne
    variables = []  # symbole terminalne
    start_symbol = ''  # symbol startowy
    grammar_type = ''  # typ gramatyki
    error = ''  # aktalny bląd
    cyclic = False  # gramatyka z cyklem?
    fixed = False  # gramatyka wymagała poprawy

    inf = ['⒨', '⒩', '⒪', '⒫', '⒬', '⒭', '⒮', '⒯', '⒰', '⒱', '⒲', '⒳',
           '⒜', '⒝', '⒞', '⒟', '⒠', '⒡', '⒢', '⒣', '⒤', '⒥', '⒦', '⒧',
           '⒴', '⒵', 'Ⓐ', 'Ⓑ', 'Ⓒ', 'Ⓓ', 'Ⓔ', 'Ⓕ', 'Ⓖ', 'Ⓗ', 'Ⓘ', 'Ⓙ',
           'Ⓚ', 'Ⓛ', 'Ⓜ', 'Ⓝ', 'Ⓞ', 'Ⓟ', 'Ⓠ', 'Ⓡ', 'Ⓢ', 'Ⓣ', 'Ⓤ', 'Ⓥ',
           'Ⓦ', 'Ⓧ', 'Ⓨ', 'Ⓩ', 'ⓐ', 'ⓑ', 'ⓒ', 'ⓓ', 'ⓔ', 'ⓕ', 'ⓖ', 'ⓗ',
           'ⓘ', 'ⓙ', 'ⓚ', 'ⓛ', 'ⓜ', 'ⓝ', 'ⓞ', 'ⓟ', 'ⓠ', 'ⓡ', 'ⓢ', 'ⓣ',
           'ⓤ', 'ⓥ', 'ⓦ', 'ⓧ', 'ⓨ', 'ⓩ', '⑴', '⑵', '⑶', '⑷', '⑸', '⑹',
           '⑺', '⑻', '⑼', '⑽', '⑾', '⑿', '⒀', '⒁', '⒂', '⒃', '⒄', '⒅', '⒆', '⒇']

    pattern = ''  # wzor jezyka

    def __init__(self):
        self.data = []
        self.rules = []
        self.str_rules = []
        self.nonTerm = []
        self.variables = []
        self.pattern = ''
        self.recursions = []
        self.start_symbol = ''
        self.grammar_type = ''
        self.cyclic = False
        self.fixed = False

    def prepare_data(self, val):  # wstępna obróbka skryptu, np. obcinanie bialych znakow
        self.data = val.splitlines()
        i = 0
        for d in self.data:
            self.data[i] = d.strip(' \t\n\r')  # usuwa białe znaki z lewej i prawej strony
            i += 1
        self.data = list(filter(None, self.data))  # tworzy przefiltrowaną listę pozbywając się pustych linii

    def check_syntax(self):  # sprawdzenie poprawności składni
        is_error = False
        i = 0  # licznik regul
        for d in self.data:
            if d.startswith("//"):  # jeśli linia zaczyna się od // to uznaj ją za komentarz i nic nie rób
                continue
            if d.count('->') != 1:  # jeżeli ilość -> nie jest równa 1
                print(self.error_list[1] + ' w wyrażeniu ' + d)
                is_error = True
                self.error = self.error_list[1] + ' w wyrażeniu ' + d
                break
            if d.endswith('.') == 0:  # jeżeli ostatni znak to nie kropka
                print(self.error_list[2] + ' w wyrażeniu ' + d)
                is_error = True
                self.error = self.error_list[2] + ' w wyrażeniu ' + d
                break

            arrow_index = d.find('->')  # pozycja symbolu ->
            left = d[0:arrow_index].strip(' \t\n\r')
            right = d[arrow_index + 2:-1].strip(' \t\n\r')  # +2 bo strzalka to 2 znaki, a -1 bo ma byc bez kropki
            right = right.replace(" ", "")

            if left.count(' ') != 0 or len(left) == 0 or left.count('.') != 0 or left.count('ε') != 0:
                # jeżeli lewa strona zawiera spacje lub kropke lub null
                print(self.error_list[0] + ' w wyrażeniu ' + d)
                is_error = True
                self.error = self.error_list[0] + ' w wyrażeniu ' + d
                break

            if i == 0:
                if len(left) > 1 or not left[0].isupper():
                    # jeżeli pierwsza regula nie zaczyna sie jedynie od symbolu startowego lub symbol jest mala litera
                    print(self.error_list[5])
                    is_error = True
                    self.error = self.error_list[5]
                    break
                else:
                    self.start_symbol = left

            if right.count('.') != 0:  # jeżeli prawa strona zawiera .
                print(self.error_list[3] + ' w wyrażeniu ' + d)
                is_error = True
                self.error = self.error_list[3] + ' w wyrażeniu ' + d
                break

            if right.count('|') == 0:  # jeżeli prawa strona nie zawiera |
                if right.strip(' \t\n\r') == '':
                    right = 'ε'  # lambda
                self.rules.append(left + '→' + right.strip(' \t\n\r'))

            else:
                rules_count = right.count('|') + 1  # liczba reguł rozdzielonych znakiem |
                right_rules = right.split('|')
                for i in range(0, rules_count):
                    if not right_rules[i].strip(' '):
                        self.rules.append(left + '→ε')  # ε czyli lambda

                    else:
                        self.rules.append(left + '→' + right_rules[i].strip(' \t\n\r'))

            for a in left:
                if a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    self.nonTerm.append(a)
            self.nonTerm = list(set(self.nonTerm))  # usuniecie duplikatow symboli nieterminalnych
            if len(self.nonTerm) > 98:  # jezeli ilosc s.nt. przekracza 98 (ze wzgledu na symbole rekurencji)
                is_error = True
                self.error = self.error_list[4]

            i += 1  # zwieksz licznik regul

        if not is_error:
            self.rules = list(set(self.rules))  # usuniecie duplikatow regul
            for r in self.rules:
                for l in r:
                    if l != '→':
                        self.variables.append(l)
            self.variables = list(set(self.variables))  # usiniecie duplikatow symb term i nieterm
            self.variables.sort()
            self.rules.sort(reverse=True)
        else:
            self.rules = []

    def test_for_type(self):  # sprawdz typ gramatyki wg hierarhii Chomsky'ego
        self.grammar_type = ''
        lr = False  # left regural
        rr = False  # right regural
        cf = False  # context-free
        cnf = False  # chomsky normal form
        gnf = False  # greibach normal form

        for r in self.rules:
            arrow_index = r.find('→')  # pozycja symbolu ->
            left = r[0:arrow_index].strip(' \t\n\r')
            right = r[arrow_index + 1:].strip(' \t\n\r')
            if len(left) > len(right):  # jezeli lewa strona jest wieksza niz prawa
                self.grammar_type = 'kombinatoryczna.'
                return self.grammar_type
            else:
                self.grammar_type = 'kontekstowa.'
                if len(left) > 1:  # jezeli lewa strona jest dluzsza niz 1 znak
                    return self.grammar_type
                else:
                    if left not in self.nonTerm:  # jezeli lewa strona to nie nieterminal
                        return self.grammar_type
                    else:
                        if len(right) == 1:  # jeżeli prawa strona to 1 znak (ten warunek nie jest ostateczny i wiążący)
                            self.grammar_type = 'prawostronnie regularna.'
                        else:
                            uc = 0  # ilosc uppercase'ów
                            for c in right:
                                if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                                    uc += 1
                            if uc == 0:  # wszystkie znaki sa male
                                self.grammar_type = 'prawostronnie regularna.'
                            else:
                                if uc == 1:
                                    if right[0].isupper():
                                        lr = True
                                    else:
                                        if right[-1].isupper():
                                            rr = True
                                        else:
                                            cf = True
                                            break
                                else:
                                    cf = True
                                    break
        if cf:
            self.grammar_type = 'bezkontekstowa'
        else:
            if lr and rr:
                self.grammar_type = 'bezkontekstowa'  # jeżeli gramatyka zawiera zarowno produkcje lr i rr to jest cf

            if lr and not rr:
                self.grammar_type = 'lewostronnie regularna.'

            if not lr and rr:
                self.grammar_type = 'prawostronnie regularna.'

        if cf or (lr and rr):  # jezeli bezkontekstowa to sprawdz czy jest w postaci normalnej chomsky'ego lub greibach
            for r in self.rules:
                arrow_index = r.find('→')  # pozycja symbolu ->
                right = r[arrow_index + 1:].strip(' \t\n\r')

                if len(right) <= 2:  # w postaci chomsky'ego reguły mogą byc w postaci a lub AA
                    if len(right) == 2:
                        if right.isupper():
                            cnf = True
                        else:
                            cnf = False
                            break
                    else:
                        if len(right) == 1:
                            if right == 'ε':
                                cnf = False
                                break
                            else:
                                if right.isupper():
                                    cnf = False
                                    break
                                else:
                                    cnf = True
                else:
                    cnf = False
                    break

            if cnf:
                self.grammar_type += " w postaci normalnej Chomsky'ego."
            else:
                for r in self.rules:
                    arrow_index = r.find('→')  # pozycja symbolu ->
                    right = r[arrow_index + 1:].strip(' \t\n\r')
                    # w postaci chomsky'ego reguły mogą byc w postaci a lub aAAAA...

                    if len(right) > 1:
                        if right[0].isupper():
                            gnf = False
                            break
                        else:
                            if right[1:].isupper():
                                gnf = True
                            else:
                                gnf = False
                                break
                    else:
                        if right[0].isupper():
                            gnf = False
                            break
                        else:
                            gnf = True
                if gnf:
                    self.grammar_type += " w postaci normalnej Greibach."
                else:
                    self.grammar_type += "."
        return self.grammar_type

    def find_pattern(self):  # wypisanie tworzenia gramatyki krok po kroku tylko dla bezkontekstowej bez wielokrt. reku.
        if self.grammar_type != 'kombinatoryczna.' and self.grammar_type != 'kontekstowa.':
            self.rules = self.fix_grammar(self.rules)
            if self.cyclic:
                return '\n\nWygenerowanie języka jest dostępne jedynie dla gramatyk niezwierających cyklów.\n\n'
            else:
                fix_msg = ''
                if self.fixed:
                    self.rules.sort(reverse=True)
                    fix_msg += 'Gramatyka zawierała reguły nieosiągalne oraz/lub reguły niepotrzebne.'
                    fix_msg += '\nZostała przekształcona do postaci:\n\n' + self.get_rules()

                normal_recursion_count = 0  # ilosc pojedynczych rekursji np S-> aS| Sa| aSa |S
                multiple_recursion_count = 0  # ilosc rekursji wielokrotnych np S-> S |SS |SSS...
                ambigous_recursion_count = 0  # ilosc rekursji niejednoznaczych np S->aSaS |SaS| aSS| aSSaSa
                for r in self.rules:
                    rcount = r.count(r[0])
                    if rcount >= 2:
                        self.recursions.append(r)
                        if rcount == 2:
                            normal_recursion_count += 1
                        else:
                            if rcount >= 3:
                                substring = ''  # pomocnicza generująca bloki typu AA AAA AAAA...
                                for i in range(0, rcount - 1):
                                    substring += r[0]
                                if r.find(substring) == -1:  # jezeli po prawej stronie jest 3xA i nie jest to blok AAA
                                    ambigous_recursion_count += 1
                                else:
                                    if len(r) - 2 == rcount - 1:
                                        multiple_recursion_count += 1
                                    else:
                                        ambigous_recursion_count += 1

                if ambigous_recursion_count != 0 or multiple_recursion_count >= 2 or (
                        multiple_recursion_count == 1 and normal_recursion_count >= 1):
                    self.pattern = "\n\nWygenerowanie języka nie jest dostępne dla gramatyk z niejednoznaczną rekurencją."
                else:
                    recursion_index = []
                    if len(list(set(self.variables) - set(self.nonTerm))) == 0:
                        self.pattern = "Zbiór reguł produkcji jest poprawny, jednak nie zawiera symboli terminalnych."
                    else:
                        self.str_rules = list(
                            set(self.rules) - set(self.recursions))  # rozdzielenie regul zwyklych od rekur.
                        if len(self.str_rules) == 0:
                            return "Zbiór reguł produkcji zawiera jedynie nieskończone rekurencje."
                        temp_pattern = self.start_symbol
                        self.pattern += "Język generowany przez podaną gramatykę:\n\n"
                        self.pattern += temp_pattern + ' → '  # poczatek wyprowadzenia wzoru
                        temp_pattern = ''
                        count = 0  # zmienna pomocnicza do poprawnego wyswietlania nawiasów i plusów
                        rec_count = 0  # ilosc rekurencji

                        for rec in self.recursions:  # dla kazdej rekurencji...
                            if rec[0] == self.start_symbol:  # jezeli dotyczy symbolu poczatkowego
                                part = rec[2:]
                                if count == 0:  # jezeli to pierwszy element to dodaj tylko nawias otwierajacy bez plusa
                                    if len(part) == part.count(self.start_symbol):  # jezeli rekurencja typu (SS)
                                        recursion_index.append(len(part) - 1)
                                        part = 'S' + self.inf[rec_count]
                                    else:
                                        for ch in self.variables:
                                            if ch in part and ch != self.start_symbol:
                                                part = part.replace(ch, ch + self.inf[rec_count])
                                        recursion_index.append(0)
                                    temp_pattern += "(" + part
                                else:  # w przeciwnym wypadku dodaj sam plus bez nawiasu
                                    if len(part) == part.count(self.start_symbol):
                                        recursion_index.append(len(part) - 1)
                                        part = 'S' + self.inf[rec_count]
                                    else:
                                        for ch in self.variables:
                                            if ch in part and ch != self.start_symbol:
                                                part = part.replace(ch, ch + self.inf[rec_count])
                                        recursion_index.append(0)
                                    temp_pattern += " + " + part
                                count += 1  # zwieksz licznik zastapien w 1 nawiasie
                                rec_count += 1  # zwieksz licznik rekurencji

                        # zrobic podmienianie startowego na reszte
                        count = 0
                        u = ''
                        if temp_pattern.count(self.start_symbol) > 0:  # jeśli jest rekurencja to podmien
                            for st in self.str_rules:  # dla kazdej normalej (nirekurencyjnej) reguły...
                                if st[0] == self.start_symbol:
                                    if count == 0:
                                        u += "(" + st[2:]
                                    else:
                                        u += " + " + st[2:]
                                    count += 1
                            u += ")"
                            temp_pattern = temp_pattern.replace(self.start_symbol, u)
                        else:  # jesli nie ma rekurencji to wypisz normalne produkcje
                            for st in self.str_rules:  # dla kazdej normalej (nirekurencyjnej) reguły...
                                if st[0] == self.start_symbol:
                                    if count == 0:
                                        temp_pattern += "(" + st[2:]
                                    else:
                                        temp_pattern += " + " + st[2:]
                                    count += 1

                        temp_pattern += ")"  # zamknij nawias
                        # temp_pattern = temp_pattern.replace(' + ?)', ')')
                        # temp_pattern = temp_pattern.replace('(? + ', '(')
                        # temp_pattern = temp_pattern.replace('+ ? +', '+')
                        self.pattern += temp_pattern

                        solution = list(temp_pattern)
                        solution[0] = '{'
                        solution[-1] = '}'
                        self.pattern += "\n\nL(G) = " + "".join(solution)
                        if len(recursion_index) > 0:
                            self.pattern += "\n\ngdzie:\n"
                            for i in range(0, len(recursion_index)):
                                if recursion_index[i] == 0:
                                    self.pattern += self.inf[i] + " = 0, 1, 2,...\n"
                                else:
                                    self.pattern += self.inf[i] + " = " + "1" + ", " + str(
                                        1 + recursion_index[i]) + ", " + str(1 + recursion_index[i] * 2) + ",...\n"

                resp = fix_msg + self.pattern
                return resp
        else:
            return '\n\nWygenerowanie języka jest dostępne jedynie dla gramatyk bezkontekstowych i regularnych.'

    def fix_grammar(self, g2fix):  # sprawdza czy sa cykle i usuwa reguły niepotrzebne oraz reguły nieosiągalne
        globalused = []
        localused = []
        actual = self.start_symbol
        temp = ''
        way = actual
        is_cycle = False
        index = 0
        comp = []
        while way and not is_cycle:
            for w in way:
                for r in g2fix:
                    if r[0] == actual:
                        part = r[2:]
                        for p in part:
                            index += 1
                            comp.append(p)
                for a in range(0, index):
                    if comp[a] != actual:
                        if comp[a] not in localused:
                            if comp[a] in self.nonTerm:
                                temp += comp[a]
                                localused.append(comp[a])
                index = 0
                globalused.append(actual)
                way = temp
                localused = []
                comp = []
                temp = []
                if way:
                    actual = way[0]
                    for elements in way:
                        if elements in globalused:
                            is_cycle = True
                else:
                    actual = ''
        if is_cycle:
            print('cykl :(')
            self.cyclic = True
        else:
            print('brak cyklu :)')

        if not is_cycle:
            while True:
                gcopy = g2fix

                useless = []
                for r in g2fix:
                    if r[0] == r[2:] and len(r) == 3:  # 3 znaki N strzalka produkcja
                        useless.append(r)
                g2fix = [item for item in g2fix if item not in useless]  # usuniecie

                for n in self.nonTerm:  # usun prod. niepotrzebne (same rekurencje)
                    rec_count = 0
                    all_count = 0
                    for r in g2fix:
                        if r[0] == n:
                            all_count += 1
                            if r[2:].count(n) >= 1:
                                rec_count += 1
                    if all_count == rec_count:
                        self.nonTerm.remove(n)
                        self.fixed = True
                        g2fix = [item for item in g2fix if item.count(n) == 0]

                for rr in g2fix:  # usun prod. nieosiągalne(nieterminal nie wystepuje nigdzie po prawej stronie)
                    useless = []
                    for n in self.nonTerm:
                        count = 0
                        if n != self.start_symbol:
                            for y in g2fix:
                                part = y[2:]
                                if n in part and y[0] != n:
                                    count += 1
                            if count == 0:
                                useless.append(n)
                                self.fixed = True
                    g2fix = [item for item in g2fix if item[0] not in useless]  # usuniecie
                    self.nonTerm = [item for item in self.nonTerm if item not in useless]
                if g2fix == gcopy:
                    break
        return g2fix

    def write_rules(self):
        for d in self.rules:
            print(d)

    def write_data(self):
        for d in self.data:
            print(d)

    def get_data(self):
        return self.data

    def get_rules(self):
        r = ''
        for a in self.rules:
            r += a + '\n'
        return r

    def get_variables(self):
        r = ''
        for a in self.variables:
            r += a + ' '
        r += '}, { '
        term = list(set(self.variables) - set(self.nonTerm))
        # for t in term:
        # if t in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        # term.remove(t)
        term.sort()
        for t in term:
            r += t + ' '
        r += "}, P, " + self.start_symbol + ">"
        return r

    def get_error(self):
        return self.error

    def get_response(self):
        response = "Gramatyka G=<{ " + self.get_variables() + " o następujących regułach produkcji:\n\n" + \
                   self.get_rules() + "\n" + self.find_pattern() + "\n\nGramatyka G jest " + self.test_for_type()

        return response

    @staticmethod
    def get_instructions():
        return "// Przykładowa gramatyka:\nS->AB|AC.\nB->BB|zx.\nA->xC|y.\nC->zB|CC.\nQ->Qt|BB|CAB."








