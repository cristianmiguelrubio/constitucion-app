/**
 * Genera icon-192.png e icon-512.png a partir del SVG.
 * Ejecutar una sola vez: node generate-icons.mjs
 * Requiere: npm install sharp
 */
import sharp from 'sharp'
import { readFileSync } from 'fs'

const svg = readFileSync('./public/icon.svg')

await sharp(svg).resize(192, 192).png().toFile('./public/icon-192.png')
console.log('✓ icon-192.png')

await sharp(svg).resize(512, 512).png().toFile('./public/icon-512.png')
console.log('✓ icon-512.png')

await sharp(svg).resize(32, 32).png().toFile('./public/favicon.ico')
console.log('✓ favicon.ico')
