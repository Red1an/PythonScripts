
/// Heading for structural elements, compliant with GOST 7.32-2019, clause 6.2.1.
/// Centered, preferrably uppercase.
#let struct-heading(body) = {
	show heading: it => align(center, it.body)
	pagebreak(weak: true)
	heading(numbering: none, body)
}

/// A combination of GOST 7.32-2019 and 2.105-2019.
#let template(
	/// Allowed to be 1em in case of large text.
	leading: 1.5em,
	/// Allowed to be more than 12pt.
	fontsize: 12pt,
	doc,
) = {
	let first-line-indent = 1.25cm
	let lineheight = 0.65em

	// GOST 7.32-2019, clause 6.1.1
	set text(
		font: "Times New Roman",
		size: fontsize,
		lang: "ru",
	)

	// GOST 7.32-2019, clause 6.1.1
	set page(
		paper: "a4",
		margin: (
			top: 2cm,
			bottom: 2cm,
			left: 3cm,
			right: 1.5cm,
		),
	)

	// GOST 7.32-2019, clause 6.1.1
	set par(
		leading: leading,
		spacing: leading,
		first-line-indent: (amount: first-line-indent, all: true),
		justify: true,
	)

	// GOST 7.32-2019, clause 6.2.3
	set heading(
		numbering: "1.1",
		hanging-indent: 0pt,
	)

	// GOST 7.32-2019, clause 6.2.3
	show heading: it => {
		let content = if it.numbering != none {
			context { counter(heading).display(it.numbering) }
			[ ]
			it.body
		} else {
			it.body
		}
		// GOST 2.105-2019, clause 6.6.3
		v(weak: true, lineheight + leading * 2)
		par(hanging-indent: it.hanging-indent, content)
	}

	// GOST 7.32-2019, clause 6.2.1
	show heading: it => pagebreak(weak: true) + it
    // эт без авто перевода на новую страницу 
   // show heading: it => v(weak: true, 2em) + it

	// GOST 7.32-2019, clause 6.2.4
	show heading: set text(size: fontsize, hyphenate: false)

	// GOST 7.32-2019, clause 6.3.1
	set page(
		numbering: "1",
		number-align: center + bottom,
	)

	// GOST 7.32-2017, clause 5.4.1
	set outline.entry(fill: repeat[.])
	set outline(title: [СОДЕРЖАНИЕ])

	// GOST 7.32-2017, clause 5.4.1
	show outline: it => context {
		set outline(indent: measure("  ").width)
		show linebreak: "."
		show heading: it => struct-heading(it.body)
		it
	}

	// GOST 7.32-2017, clause 6.5.7 and 6.6.3
	set figure.caption(separator: [ --- ])

	// GOST 7.32-2017, clause 6.5.8
	show figure.caption: set par(leading: 1em)
	set figure(gap: leading)

	// GOST 7.32-2017, clause 6.5.8
	show figure.caption: set text(hyphenate: false)

	// Display caption even without a name
	show figure.where(caption: none): set figure(caption: [])
	show figure.where(caption: none): set figure.caption(separator: [])

	show figure: it => {
		it
		v(weak: true, lineheight + leading * 2)
	}

	// GOST 7.32-2017, clause 6.5.1
	// Display listings as images, except they are breakable
	show figure.where(kind: raw): set figure(kind: image, supplement: [Рисунок])
	show figure.where(kind: raw): set block(width: 100%, breakable: true)

	// GOST 7.32-2017, clause 6.6.3
	show figure.where(kind: table): set figure.caption(position: top)
	show figure.caption.where(kind: table): align.with(left);

	set table(
		inset: leading / 2,
	)

	// GOST 7.32-2017, clause 6.5.1
	show figure.where(kind: image): set figure(supplement: [Рисунок])

	// GOST 7.32-2017, clause 6.8.4
	show ref: it => {
		let equation-ref(it) = {
			let el = it.element
			link(el.location(), {
				numbering(el.numbering, ..counter(math.equation).at(el.location()))
			})
		}

		if it.element != none and it.element.func() == math.equation {
			equation-ref(it)
		} else {
			it
		}
	}

	// GOST 7.32-2017, clause 6.8.3
	set math.equation(
		numbering: "(1)",
	)

	// GOST 7.32-2017, clause 6.4.6
	set list(
		marker: ([--], [•]),
	)

	// GOST 7.32-2017, clause 6.4.6
	// Displaying lists as paragraphs
	show list: it => context {
		let list-counter = counter("list-counter")

		let marker = it.marker
		// Циклично выбираем маркер из списка
		if type(marker) == array {
			let i = calc.rem-euclid(list-counter.get().at(0), marker.len())
			marker = marker.at(i)
		} else if type(marker) == function {
			marker = marker(list-counter.get().at(0))
		}
		list-counter.step()
		for item in it.children {
			block({
				h(it.indent)
				marker
				h(it.body-indent)
				item.body
				parbreak()
			})
		}
		list-counter.update(x => x - 1)
	}

	set enum(numbering: (x, ..xs) => {
		if xs.pos().len() > 0 {
			numbering("a)", xs.pos().last())
		} else {
			numbering("1)", x)
		}
	})

	// GOST 7.32-2017, clause 6.4.6
	// Displaying enums as paragraphs
	show enum: it => context {
		let enum-counter = counter("enum-counter")

		for item in it.children {
			block({
				enum-counter.update((..xs, x) => xs.pos() + (item.at(default: x + 1, "number"),))

				context {
					h(it.indent)
					numbering(it.numbering, ..enum-counter.get())
					h(it.body-indent)
					enum-counter.update((..xs) => xs.pos() + (0,))
				}
				item.body
				parbreak()
				enum-counter.update((..xs, _) => xs.pos())
			})
		}
		enum-counter.update((..xs, _) => xs.pos() + (0,))
	}

	// GOST 7.32-2017, clause 6.7.4
	set footnote.entry(
		indent: first-line-indent,
	)

	// GOST 7.32-2017, clause 6.16
	show bibliography: it => {
		show heading: align.with(center)
		show block: it => it.body + parbreak()
		it
	}

	doc
}