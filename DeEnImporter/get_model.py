
model_name = "Reversed-Importer"


def get_model(col):  # mm = ModelManager
    mm = col.models

    m = mm.byName(model_name)
    if m:
        mm.setCurrent(m)
        return m

    m = create_model(mm)
    t1, t2 = create_templates(mm)
    set_css(m)

    # adding template and model
    mm.addTemplate(m, t1)
    mm.addTemplate(m, t2)
    mm.add(m)

    mm.setCurrent(m)
    mm.save()
    return m


def create_model(mm):
    m = mm.new(model_name)

    fm = mm.newField("German")
    mm.addField(m, fm)
    fm = mm.newField("English")
    mm.addField(m, fm)
    fm = mm.newField("German Examples")
    mm.addField(m, fm)
    fm = mm.newField("English Examples")
    mm.addField(m, fm)
    fm = mm.newField("Media")
    mm.addField(m, fm)

    return m


def create_templates(mm):
    t1 = mm.newTemplate("Card 1")

    t1['qfmt'] = """
        <p id="english">{{English}}</p>
        <p id="example">{{English Examples}}</p>
        """

    t1['afmt'] = """
        {{FrontSide}}
        <hr id=answer>
        <p id="german">{{German}}</p>
        <p id="example">{{German Examples}}</p>
        {{Media}}
        """

    t2 = mm.newTemplate("Card 2")

    t2['qfmt'] = """
        <p id="german">{{German}}</p>
        """

    t2['afmt'] = """
        {{FrontSide}}
        <hr id=answer>
        <p id="german">{{English}}</p>
        <p id="example">{{German Examples}}</p>
        {{Media}}
        """

    return t1, t2


def set_css(m):

    m['css'] = """.card {
     font-family: arial;
     font-size: 20px;
     text-align: center;
     color: black;
     background-color: white;
    }

    #example {
     color: blue;
    }
    """
