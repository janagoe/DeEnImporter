
model_name = "Vocab-Importer-Reversed"


def get_model(col):  # 'mm' means ModelManager
    """
    Searching for the model to use and creating it, if it doesn't exist yet.
    :param col: Anki collection
    :return: the model to use
    """
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

    fm = mm.newField("FromLang")
    mm.addField(m, fm)
    fm = mm.newField("DestLang")
    mm.addField(m, fm)
    fm = mm.newField("FromLang Examples")
    mm.addField(m, fm)
    fm = mm.newField("DestLang Examples")
    mm.addField(m, fm)
    fm = mm.newField("FromAudio")
    mm.addField(m, fm)
    fm = mm.newField("DestAudio")
    mm.addField(m, fm)
    fm = mm.newField("FromImages")
    mm.addField(m, fm)
    fm = mm.newField("DestImages")
    mm.addField(m, fm)

    return m


def create_templates(mm):
    t1 = mm.newTemplate("Card 1")
    t1['qfmt'] = """
        <p id="destlang">{{DestLang}}</p>
        <p id="example">{{DestLang Examples}}</p>
        {{DestImages}}
        {{DestAudio}}
        """
    t1['afmt'] = """
        {{FrontSide}}
        <hr id=answer>
        <p id="fromlang">{{FromLang}}</p>
        <p id="example">{{FromLang Examples}}</p>
        {{FromImages}}
        {{FromAudio}}
        """

    t2 = mm.newTemplate("Card 2")
    t2['qfmt'] = """
        <p id="fromlang">{{FromLang}}</p>
        <p id="example">{{FromLang Examples}}</p>
        {{FromImages}}
        {{FromAudio}}
        """
    t2['afmt'] = """
        {{FrontSide}}
        <hr id=answer>
        <p id="destlang">{{DestLang}}</p>
        <p id="example">{{DestLang Examples}}</p>
        {{DestImages}}
        {{DestAudio}}
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
