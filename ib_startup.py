import datetime

while True:
    hover("1703102694235.png")
    #if exists("1703102694235.png"):
    x = datetime.datetime.now()
    if x.hour == 13 and x.minute == 7:
        doubleClick(Pattern("1703271521178.png").targetOffset(-4,-35))
        while True:
            if exists("1703103806160.png"):
                click(Pattern("1703103806160.png").targetOffset(-110,-12))
                sleep(3)
                type("greatdogsite")
                type(Key.TAB)
                sleep(3)
                type("QX$jg^NB8<{k(Zrd-[M.j2)D,S&LUF")      
                type(Key.ENTER)
                break

        while True:
            if exists("1703104271016.png"):
                wait(30)
                click(Pattern("1703104271016.png").targetOffset(-34,92))
                wait(10)
                break

        click(Pattern("1703104383603.png").similar(0.75))
        wait(5)
        click(Pattern("1703104383603.png").targetOffset(-9,-60))
        type("py algo.py")
        wait(3)
        type(Key.ENTER)
        break

    hover("1703124270977.png")
    click(Pattern("1703124270977.png").targetOffset(-6,-86))
    wait(19)

    