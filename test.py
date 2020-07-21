class Tag:
    def __init__(self, tag, is_single = False, toplevel = False, klass = None, **kwargs):
        self.tag = tag
        self.is_single = is_single
        self.toplevel = toplevel
        self.attributs = {}
        self.text = ""
        self.childrens = []

        if klass is not None:
            self.attributs["class"] = " ".join(klass)
        for attr, val in kwargs.items():
            self.attributs[attr] = val

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def __str__(self):
        attrs = []
        for attr, val in self.attributs.items():
            attrs.append("%s='%s'"%(attr, val))
        attrs = " ".join(attrs)
        if self.childrens:
            op = "<{tag} {attrs}>\n".format(tag = self.tag, attrs = attrs)
            inter = "%s"%self.text
            for child in self.childrens:
                inter += str(child)
            ed = "</%s>\n"%self.tag
            return op + inter + ed
        else:
            if self.is_single:
                return "<{tag} {attrs}>\n".format(tag = self.tag, attrs = attrs)
            else:
                return "<{tag} {attrs}>{text}</{tag}>\n".format(tag = self.tag, attrs = attrs, text = self.text)

    def __add__(self, other):
        self.childrens.append(other)
        return self

# Делаем класс HTML наследником Tag
class HTML(Tag):
    def __init__(self, output = None): # Убираем возможность ввода доп параметров
        self.tag = "html" # Добавляем готовый tag
        # Присваиваем готовые значения для is_single и toplevel
        self.is_single = False
        self.toplevel = True

        self.output = output
        self.childrens = []
        self.attributs = {}
        self.text = ""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self.output is None: # Указываем условие, если output = None,то просто вывудим все через print
            if self.toplevel:
                print("<%s>" % self.tag)
                for child in self.childrens:
                    print(child)
                print("</%s>" % self.tag)
        else: # Иначе записываем рузультат в нужный нам файл, указанный в значении output
            with open(self.output, "w") as file_op:
                file_op.write(str(self))

# Делаем класс TopLevelTag наследником Tag
class TopLevelTag(Tag):
    def __init__(self, tag): # Убираем возможность ввода доп параметров
         # Присваиваем готовые значения для is_single и toplevel
        self.is_single = False
        self.toplevel = False

        self.tag = tag
        self.childrens = []
        self.attributs = {}
        self.text = ""

if __name__ == "__main__":
    with HTML(output = None) as doc: # Здесь можно вместо None указать путь к файлу, в который вы хотите вывести результат
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "Hellow"
                head += title
            doc += head
        with TopLevelTag("body") as body:
            with Tag("h1", klass = ("main-text",)) as h1:
                h1.text = "Test"
                body += h1
            with Tag("div", klass = ("container", "container-fluid"), id = "lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "Another test"
                    div += paragraph
                with Tag("img", is_single = True, src = "/icon.png", data_image = "responsive") as img:
                    div += img
                body += div
            doc += body
