#set page(margin: (left: 3cm, right: 1cm, y: 2cm))
#set text(size: 14pt, font: "Times New Roman", lang: "ru")
#set par(justify: true)

#import "title.typ": title
#import "template.typ": template, struct-heading

#title( 
  "41", // кафедра
  "...", // название лабы 
  "...", // название предмета
  "4316", // группа
  "М.С. Пронь", // студент
  "...", // ФИО препода
  "..." // должность
)

#show: doc => template(doc)

#outline()

= Цель работы

= Вывод
