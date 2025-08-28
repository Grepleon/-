import io
import tokenize as std_tokenize  # Используем псевдоним для модуля


class LAG:

    def __init__(self):
        self.variables = []
        self.tokens = []
        self.f = []
        self.cod = """  

Space = " ";   
K = "Hello" + Space;
~> K + "world. K";

a = 5;
~> "Введите число:";
~< b;
~> "Сумма: " + str(a+int(b));

~? int(b) == 5;
    ~> "Вы ответили так же, как и я в первый раз";
#;

!~? int(b) == 2;
    ~> "Вы ответили так же, как и я во второй раз";
#;

!~ e;
    ~> "Ну, ты и дурак"
#;

n = 2;

@? int(n) != 10;

    ~> "Угадай число";
    ~< n;
    ~> "Вы ввели " + str(n);
#;

~> "Верно! Это было 10!";

N = [1, 2, 3];

~> N;
N ~>> 4;
~> N;
N ~<< 0;
~> N;

i = 0;
c = 0;
@? i < 3;
    i = i + 1;
    ~< c;
    ~> str(i) + ". " + str(c);
#;


"""

    def T2(self, F):
        F = str(F)
        if '"' in F or "'" in F:
            return "str"
        else:

                return "int"



    def Dx2(self):
        f2 = []
        for i in self.tokens:
            if i == "#;":
                self.f.append(f2.copy())
                f2 = []
                f2.append('#')
                f2.append(";")
                self.f.append(f2.copy())
                f2 = []
            if i not in [";", "\n"]:
                if i.count(' ') != len(i):  # Эта проверка удаляет строки с пробелами
                    if i != "#;":
                        f2.append(i)

            else:
                 if i == ";":
                    if f2:  # Добавляем только непустые списки
                        self.f.append(f2.copy())
                    f2 = []
       # print(self.f)

    def cods(self):
        #print(self.cod)
        def custom_tokenize(code_str):
            # Проверка типа ввода
            if not isinstance(code_str, str):
                raise ValueError("Input must be a string")

            # Все операторы, которые должны оставаться слитными
            MULTI_CHAR_OPS = {
                "=", "+", "-", "*", "/", "**", "/*", "//", "%", "++", "--",
                "==", "!=", ">", "<", ">=", "<=",
                "~?", "!~", "!~?", "^?", "@?", "@>", "<~", "#>", "#",
                "~>", "~>>", "~<", "~<<",
                ";", "~~", ":"
            }

            tokens = []
            try:
                # Подготовка потока для токенизатора
                code_bytes = code_str.encode('utf-8')
                stream = io.BytesIO(code_bytes)

                # Получаем токены стандартным токенизатором
                for tok in std_tokenize.tokenize(stream.readline):
                    # Пропускаем служебные токены
                    if tok.type in {std_tokenize.ENCODING, std_tokenize.ENDMARKER}:
                        continue

                    tokens.append(tok.string)

            except std_tokenize.TokenError as e:
                raise ValueError(f"Tokenization error: {e}")

            # Второй проход для склейки операторов
            i = 0
            result = []
            while i < len(tokens):
                current = tokens[i]

                # Проверяем возможные операторы от самых длинных (4 символа) до 1
                matched = False
                for length in range(4, 0, -1):
                    if i + length <= len(tokens):
                        candidate = ''.join(tokens[i:i + length])
                        if candidate in MULTI_CHAR_OPS:
                            result.append(candidate)
                            i += length
                            matched = True
                            break

                if not matched:
                    result.append(current)
                    i += 1

            return result

        # Получаем строку для токенизации
        if not isinstance(self.cod, str):
            if callable(self.cod):
                code_str = self.cod()
            else:
                code_str = str(self.cod)
        else:
            code_str = self.cod

        self.tokens = custom_tokenize(code_str)
       # print(self.tokens)


        #self.tokens)

    def Code(self):
        commands = [
            "=", "+", "-", "*", "/", "**", "/*", "//", "%", "++", "--",
            "==", "!=", ">", "<", ">=", "<=",
            "~?", "!~", "!~?", "^?", "@?", "@>", "<~", "#>", "#",
            "~>", "~>>", "~<", "~<<",
            "int", "float", "str", "bool", "search",
            ";", "~~", ":"
        ]
        U = [True, 0]
        If = 0
        Wh = [0,[]]
        i = -1
        while i < len(self.f) - 1:

            i += 1
            if U[1] == 0:
                U[0] = True

            n = 0
            instr = None
            Var = []
            current_line = self.f[i]

            for j in current_line:
                n += 1




                if n == 1:
                    if j in commands:
                        instr = j

                        if j == "~?":
                            U[1] += 1

                        if j == "!~":
                            U[1] += 1

                        if j == "!~?":
                            U[1] += 1

                        if j == "@?":
                            U[1] += 1

                        if j == "^?":
                            U[1] += 1

                        if j == "#":
                            U[1] -= 1

                            if Wh[0] ==1:
                                i = Wh[1] - 1


                    else:
                        Var = [j]

               # if Wh[0] == 1:
                   # print(self.f[i], '\n', U, Wh)
                if instr == "@?" and n == 2 and U[0]:
                    # Собираем всё что после ~> в одну строку
                    Full = ''
                    for I in range(1, len(self.f[i])):
                        J = self.f[i][I]

                        for k in self.variables:
                            if k[0] == J:
                                J = k[1]
                                if k[2] == 'str':
                                    J = '"' + J + '"'

                        Full += str(J)
                    #print(Full)
                    #print(Full, eval(Full))
                    U[0] = eval(Full)
                   # print(U[0])
                    if U[0]:
                        a = []
                        a2 = []
                        l = i

                        Wh = [1, l]
                    else:
                        Wh = [0, []]



                if instr == "~?" and n == 2 and U[0]:
                    # Собираем всё что после ~> в одну строку
                    Full = ''
                    for I in range(1, len(self.f[i])):
                        J = self.f[i][I]

                        for k in self.variables:
                            if k[0] == J:
                                J = k[1]
                                if k[2] == 'str':
                                    J = '"' + J + '"'

                        Full += str(J)
                    #print(Full)
                    U[0] = eval(Full)

                    if U[0] == True:
                        If = 1
                    else:
                        If = 0

                if instr == "!~" and n == 2 and U[0]:
                    U[0] = If == 1
                    if j == "e":
                        U[0] = If == 0
                    elif j == 'a':
                        U[0] = True
                    elif j == 'i':
                        U[0] = If == 1
                    elif j == "c":
                        U[0] = False

                if instr == "!~?" and n == 2 and U[0]:
                    # Собираем всё что после ~> в одну строку
                    Full = ''
                    for I in range(1, len(self.f[i])):
                        J = self.f[i][I]

                        for k in self.variables:
                            if k[0] == J:
                                J = k[1]
                                if k[2] == 'str':
                                    J = '"' + J + '"'

                        Full += str(J)
                    # print(Full)
                    U[0] = eval(Full) if If == 0 else False
                    if If == 0:
                        if U[0] == True:
                            If = 1
                        else:
                            If = 0
                    else:
                        If = 1


                if instr == "~<" and n == 2 and U[0]:

                    self.variables.insert(0, [j, input(), self.T2(j)])

                if instr == "~>" and n >= 2 and U[0]:
                    # Собираем всё что после ~> в одну строку
                    Full = ''
                    for I in range(1, len(self.f[i])):
                        J = self.f[i][I]

                        for k in self.variables:
                            if k[0] == J:
                                J = k[1]
                                if k[2] == 'str':
                                    J = '"' + J + '"'

                        Full += str(J)
                  # print(Full)
                #    print(self.variables)
                    print(eval(Full))


                    #print(Full)  # Выводим в консоль
                    break

                if n == 2 and len(Var ) == 1:
                    instr = j


                if len(Var) == 1 and n >= 3 and U[0]:
                    if instr == "=":
                        # Собираем всё что после ~> в одну строку
                        Full = ''
                        for I in range(2, len(self.f[i])):
                            J = self.f[i][I]

                            for k in self.variables:
                                if k[0] == J:
                                    J = k[1]
                                    if k[2] == 'str':
                                        J = '"' + J + '"'

                            Full += str(J)
                        #(Full)
                        self.variables.insert(0, [Var[0], eval(Full), self.T2(Full)])
                        break

                        # print(Full)  # Выводим в консоль
                    if instr == "~>>":
                        # Собираем всё что после ~> в одну строку
                        Full = ''
                        for I in range(2, len(self.f[i])):
                            J = self.f[i][I]

                            for k in self.variables:
                                if k[0] == J:
                                    J = k[1]
                                    if k[2] == 'str':
                                        J = '"' + J + '"'

                            Full += str(J)
                        # (Full)
                        for k in self.variables:

                            if k[0] == Var[0]:
                                J = k[1]
                                self.variables.remove(k)
                                if True:
                                    J.append(eval(Full))
                                    self.variables.insert(0, [Var[0], J, self.T2(Full)])

                        break

                    if instr == "~<<":
                        # Собираем всё что после ~> в одну строку
                        Full = ''
                        for I in range(2, len(self.f[i])):
                            J = self.f[i][I]

                            for k in self.variables:
                                if k[0] == J:
                                    J = k[1]
                                    if k[2] == 'str':
                                        J = '"' + J + '"'

                            Full += str(J)
                        # (Full)
                        for k in self.variables:

                            if k[0] == Var[0]:
                                J = k[1]
                                self.variables.remove(k)
                                if True:
                                  #  print(J)
                                    J.pop(eval(Full))
                                  #  print(J)
                                    self.variables.insert(0, [Var[0], J, self.T2(Full)])

                        break




A = LAG()
A.cods()
A.Dx2()
A.Code()
