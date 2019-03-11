const fs = require('fs-extra');
const { promisify } = require('util');
const request = require('request');
const get = promisify(request.get);
const cheerio = require('cheerio');
const argv = require('yargs').argv;

const tablon = argv.tablon;
const hilo = argv.hilo;
const url = `https://www.hispachan.org/${tablon}/res/${hilo}.html`;

async function main() {
  try {
    const response = await get(url);

    let $ = cheerio.load(response.body);

    const imagenes = $('img.thumb').map((i, el) => {
      return el.attribs.src.replace('thumb', 'src').replace('s.jpg', '.jpg');
    });

    await fs.ensureDir(`img/${tablon}/${hilo}`);

    for (let i = 0; i < imagenes.length; i++) {
      console.log(`Descargando imagen: ${i+1}/${imagenes.length}`);
      
      request(imagenes[i]).pipe(fs.createWriteStream(`img/${tablon}/${hilo}/${i}.jpg`));
    }
  } catch (err) {
    console.error('Hubo un error \n', err);
  }
}

main();