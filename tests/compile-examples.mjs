// Syntax-check original fenced Vue examples with the consumer's installed compiler.
// This does not bundle, copy, or execute CoreUI Pro application code.
import { readFileSync, readdirSync } from 'node:fs'
import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { createRequire } from 'node:module'

const application = process.argv[2]
if (!application) throw new Error('Usage: node tests/compile-examples.mjs /path/to/licensed-vue-app')
const requireFromApp = createRequire(resolve(application, 'package.json'))
const { parse, compileScript, compileTemplate, compileStyle } = requireFromApp('@vue/compiler-sfc')
const exampleDir = resolve(dirname(fileURLToPath(import.meta.url)), '../skills/coreui-pro/examples')
let checked = 0
for (const file of readdirSync(exampleDir).filter((file) => file.endsWith('.md'))) {
  const text = readFileSync(resolve(exampleDir, file), 'utf8')
  for (const [index, block] of [...text.matchAll(/```vue\n([\s\S]*?)```/g)].entries()) {
    const id = `example-${checked}`
    const filename = `${file}-${index}.vue`
    const { descriptor, errors } = parse(block[1], { filename })
    if (errors.length) throw new Error(`${filename}: ${errors.join('\n')}`)
    const script = compileScript(descriptor, { id })
    const template = compileTemplate({ source: descriptor.template.content, filename, id, compilerOptions: { bindingMetadata: script.bindings } })
    if (template.errors.length) throw new Error(`${filename}: ${template.errors.join('\n')}`)
    for (const style of descriptor.styles) {
      const result = compileStyle({ source: style.content, filename, id, scoped: style.scoped })
      if (result.errors.length) throw new Error(`${filename}: ${result.errors.join('\n')}`)
    }
    checked++
  }
}
if (checked !== 7) throw new Error(`Expected seven SFC examples, found ${checked}`)
console.log(`PASS: ${checked} original Vue SFC blocks parse and compile (syntax only; no runtime claim)`)
