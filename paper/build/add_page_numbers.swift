import Foundation
import CoreGraphics
import CoreText

// Usage: swift add_page_numbers.swift <in.pdf> <out.pdf> [start_page]
let args = CommandLine.arguments
guard args.count >= 3 else {
    print("usage: add_page_numbers.swift <in.pdf> <out.pdf> [start]")
    exit(1)
}
let inURL = URL(fileURLWithPath: args[1])
let outURL = URL(fileURLWithPath: args[2])
let startPage = args.count > 3 ? (Int(args[3]) ?? 1) : 1

guard let doc = CGPDFDocument(inURL as CFURL) else {
    print("cannot open input pdf")
    exit(1)
}
let n = doc.numberOfPages
var mediaBox = doc.page(at: 1)!.getBoxRect(.mediaBox)

guard let consumer = CGDataConsumer(url: outURL as CFURL),
      let ctx = CGContext(consumer: consumer, mediaBox: &mediaBox, nil) else {
    print("cannot create output pdf")
    exit(1)
}

let font = CTFontCreateWithName("Times New Roman" as CFString, 8.5, nil)
let attrs: [NSAttributedString.Key: Any] = [
    NSAttributedString.Key(kCTFontAttributeName as String): font,
    NSAttributedString.Key(kCTForegroundColorAttributeName as String): CGColor(red: 0.25, green: 0.25, blue: 0.25, alpha: 1.0),
]

for i in 1...n {
    guard let page = doc.page(at: i) else { continue }
    let box = page.getBoxRect(.mediaBox)
    ctx.beginPDFPage(nil)
    ctx.saveGState()
    ctx.drawPDFPage(page)
    ctx.restoreGState()

    if i >= startPage {
        let label = "\(i) / \(n)"
        let attr = NSAttributedString(string: label, attributes: attrs)
        let line = CTLineCreateWithAttributedString(attr)
        var ascent: CGFloat = 0
        var descent: CGFloat = 0
        var leading: CGFloat = 0
        let width = CGFloat(CTLineGetTypographicBounds(line, &ascent, &descent, &leading))
        ctx.textPosition = CGPoint(x: (box.width - width) / 2.0, y: 16.0)
        CTLineDraw(line, ctx)
    }
    ctx.endPDFPage()
}
ctx.closePDF()
print("wrote \(outURL.path) with \(n) pages")
