# Akce

<div class="lead" markdown="1">
Srazy, konference, workshopy. Vše, co se v ČR děje kolem jazyka Python, na jednom místě.
</div>

[Chci uspořádat sraz v mém městě](https://docs.pyvec.org/guides/meetup.html)

## Všechny akce {: #akce }

-   **Pravidelné akce** lze přidat přes tzv.
    [iCal](https://cs.wikipedia.org/wiki/ICalendar) export. Ten může
    generovat přímo vaše webová stránka (jako v případě
    [pyvo.cz](https://pyvo.cz)), nebo jej lze vytáhnout z nějaké služby
    (Google Calendar, meetup.com). URL exportu pak na náš web [přidejte pomocí Pull Requestu](https://github.com/pyvec/python.cz/edit/master/pythoncz/static/data/events_feeds.yml).
-   **Jednorázové akce** lze přidat přes kalendář [Czech Python Events](https://calendar.google.com/calendar/embed?src=kfdeelic1a13jsp7jvai861vfs%40group.calendar.google.com&ctz=Europe%2FPrague).
    Do kalendáře má přístup mnoho z organizátorů existujících Python
    akcí, takže je poproste, ať vaši akci přidají, nebo napište na
    <info@pyvec.org>. První URL z popisu události se zde zobrazí jako
    odkaz.

## Kalendář

<ul>
{% for event in events %}
    <li{% if event.is_tentative %} class="tentative"{% endif %}>
        <strong>
            {% if event.url %}
                <a href="{{ event.url }}">{{ event.name }}</a>
            {% else %}
                {{ event.name }}
            {% endif %}
        </strong>
        <br>
        {{ "{:%-d.%-m.%-Y}".format(event.starts_at) }}
        {% if event.location %}
            <br>{{ event.location }}
            <br>
            <a href="https://mapy.cz/zakladni?q={{ event.location|urlencode }}" target="_blank" rel="noopener">Mapy.cz</a>
            <a href="https://www.google.com/maps?q={{ event.location|urlencode }}" target="_blank" rel="noopener">Google Mapy</a>
        {% endif %}
    </li>
{% endfor %}
</ul>

[iCal na všechny akce](/events.ics)
