// Local development only; production remains GitHub Pages.
import http from 'node:http';
import {readFile, stat} from 'node:fs/promises';
import {resolve, extname, sep} from 'node:path';
const args = process.argv.slice(2);
const port = Number(args[args.indexOf('--port') + 1]) || 3000;
const host = args.includes('--host') ? args[args.indexOf('--host') + 1] : '127.0.0.1';
const root = process.cwd();
const types = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.svg':'image/svg+xml','.md':'text/plain; charset=utf-8'};
http.createServer(async (req,res) => {
  try {
    const path = decodeURIComponent(new URL(req.url,'http://local').pathname);
    if (path.split('/').some(x=>x.startsWith('.'))) throw new Error('private');
    let file = resolve(root,'.'+path);
    if (!file.startsWith(root+sep) && file !== root) throw new Error('path');
    if ((await stat(file)).isDirectory()) file = resolve(file,'index.html');
    res.setHeader('Content-Type',types[extname(file)] || 'text/plain; charset=utf-8');
    res.setHeader('Cache-Control','no-store');
    res.end(await readFile(file));
  } catch {res.statusCode=404;res.end('Not found');}
}).listen(port,host,()=>console.log(`Local: http://${host}:${port}`));
