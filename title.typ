#let title(
    faculty_number,
  lab_title,
  course_title,
  student_group,
  student_name,
  chief_name,
  chief_position,

  city: "Санкт-Петербург"
) = [
  #set align(center)
  #set block(above: 12pt)

  #let inline(body) = box(baseline: 12pt)[#body]
  #let undertitle(title, width: auto, body) = {
    layout(size => {
      stack(
        dir: ttb,
        body,
        block(inset: (y: 3pt), 
          line(length: 
            if width == auto { 
              measure(body).width 
            } else { width },
            stroke: .5pt
          ),
        ),
        text(size: 9pt)[(#title)]
      )
    })
  }

  #grid(
    rows: (auto, auto, auto, auto, auto, auto, auto),
    [
      #text(size: 12pt)[#text(12pt)[ГУАП]] \
      #block(above: 10pt)[#text(12pt)[КАФЕДРА № #faculty_number]]

      #block(above: 40pt, width: 100%)[
        #set align(left)
        #text(size: 12pt)[ОТЧЕТ] \
        #block(above: 10pt)[#text(12pt)[ЗАЩИЩЕН С ОЦЕНКОЙ]]
        #block(above: 16pt)[#text(12pt)[ПРЕПОДАВАТЕЛЬ]]
      ]

   #grid(
    gutter: 20pt,
    columns: (1fr, 1fr, 1fr),
      stack(
          dir: ttb,
          spacing: 6pt,
          text(12pt)[#chief_position],
          line(length: 100%, stroke: 0.5pt),
          text(10pt)[должность, уч. степень, звание]
        ),
      stack(
          dir: ttb,
          spacing: 6pt,
          text(12pt)[ㅤ],
          line(length: 100%, stroke: 0.5pt),
          text(10pt)[подпись, дата]
        ),
              stack(
          dir: ttb,
          spacing: 6pt,
          text(12pt)[#chief_name],
          line(length: 100%, stroke: 0.5pt),
          text(10pt)[инициалы, фамилия]
        ),
    )

    
      #block(above: 130pt)[
        #text(size: 14pt)[ОТЧЕТ О ЛАБОРАТОРНОЙ РАБОТЕ]
      ]

      #block(above: 40pt)[
        #text(size: 14pt)[#lab_title]
      ]

      #block(above: 20pt)[
        #text(size: 12pt)[по курсу:]
      ]

      #block(above: 16pt)[
        #text(size: 14pt)[#course_title]
      ]

      #block(above: 200pt, width: 100%)[
        #set align(left)
        #text(size: 12pt)[РАБОТУ ВЫПОЛНИЛ]
      ]

    #grid(
    gutter: 20pt,
    columns: (2fr, 1fr, 1fr),
    stack(
      dir: ltr,
      spacing: 26pt,
      text(12pt)[СТУДЕНТ гр. №],  
      stack(
          dir: ttb,
          spacing: 6pt,
          text(12pt)[#student_group],
          line(length: 50%, stroke: 0.5pt),
        )),
    stack(
          dir: ttb,
          spacing: 6pt,
          text(12pt)[ㅤ],
          line(length: 100%, stroke: 0.5pt),
          text(10pt)[подпись, дата]
      ),
    stack(
          dir: ttb,
          spacing: 6pt,
          text(12pt)[#student_name],
          line(length: 100%, stroke: 0.5pt),
          text(10pt)[инициалы, фамилия]
      ),
    )


      #block(above: 60pt)[
        #text(size: 11pt)[#city, #datetime.today().year()]
      ]
    ]
  )
]