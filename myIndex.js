const fs = require('fs-extra');
const { promisify } = require('util');
const request = require('request');
const get = promisify(request.get);
const cheerio = require('cheerio');
const argv = require('yargs').argv;

const tablon = argv.tablon;
const hilo = argv.hilo;
const url = `https://www.hispachan.org/${tablon}/res/${hilo}.html`;

//I make a main function and call it that way I have access to async/await
//there are other ways to do that (called an IIFE), but this is easy to understand
main();
async function main() {
  try {
    const response = await get(url);

    let $ = cheerio.load(response.body);

    //I use the map function instead of each, that way I don't need 
    //to worry about doing a .push() to add the strings to an array
    const imagenes = $('img.thumb').map((i, el) => {
      return el.attribs.src.replace('thumb', 'src').replace('s.jpg', '.jpg');
    });

    //ensureDir is an fs-extra method which does exactly what you were doing in just 1 line
    await fs.ensureDir(`img/${tablon}/${hilo}`)

    //normally I wouldn't want to use a normal for loop, but Cheerio.map() returns a 
    //cheerio object instead of an array, so this will have to do.
    for (let i = 0; i < imagenes.length; i++) {
      request(imagenes[i]).pipe(fs.createWriteStream(`img/${tablon}/${hilo}/${i}.jpg`));
    }
  } catch (err) {
    console.error('Hubo un error \n', err);
  }
}
