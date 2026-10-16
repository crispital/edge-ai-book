const fs = require('fs');
const path = require('path');
const packages = process.argv[2];
const sharp = require(path.join(packages, 'sharp'));
const { chromium } = require(path.join(packages, 'playwright'));
const { instance } = require(path.join(packages, '@viz-js/viz'));

(async () => {
    const folder = __dirname;
    const dot = fs.readFileSync(path.join(folder, 'fig_02_06_01_PyTorch_FX.dot'), 'utf8');
    const viz = await instance();
    const svg = viz.renderString(dot, { format: 'svg' }); // SVG只在内存中传递，不保存文件。
    const browser = await chromium.launch({ channel: 'msedge', headless: true });
    try {
        const page = await browser.newPage({ deviceScaleFactor: 2 });
        await page.setContent(svg);
        await page.evaluate(() => document.fonts.ready);
        const checks = await page.evaluate(() => Array.from(document.querySelectorAll('g.node')).map(node => {
            const frame = node.querySelector('path,polygon,ellipse').getBBox();
            const texts = Array.from(node.querySelectorAll('text')).map(text => text.getBBox());
            return {
                node: node.querySelector('title').textContent,
                fits: texts.every(text => text.x >= frame.x + 2 && text.x + text.width <= frame.x + frame.width - 2
                    && text.y >= frame.y && text.y + text.height <= frame.y + frame.height),
            };
        }));
        if (checks.some(check => !check.fits)) throw new Error(JSON.stringify(checks));
        const leftFile = path.join(folder, 'fig_02_06_01_PyTorch_FX.png');
        await page.locator('svg').screenshot({ path: leftFile }); // 浏览器用同一字体计算并绘制文字。
        const panelHeight = 1000;
        const left = await sharp(leftFile).resize({ height: panelHeight }).toBuffer({ resolveWithObject: true });
        const right = await sharp(path.join(folder, 'fig_02_06_01_ONNX_Netron.png'))
            .trim().resize({ height: panelHeight }).toBuffer({ resolveWithObject: true });
        const splitPanel = async image => {
            const { data, info } = await sharp(image).removeAlpha().raw().toBuffer({ resolveWithObject: true });
            let best = { row: Math.floor(info.height / 2), score: Infinity };
            for (let row = Math.floor(info.height * 0.40); row < info.height * 0.60; row++) {
                let ink = 0;
                for (let col = 0; col < info.width; col++) {
                    const offset = (row * info.width + col) * info.channels;
                    if (data[offset] + data[offset + 1] + data[offset + 2] < 700) ink++;
                }
                const score = ink * 100 + Math.abs(row - info.height / 2);
                if (score < best.score) best = { row, score };
            }
            return [
                await sharp(image).extract({ left: 0, top: 0, width: info.width, height: best.row }).toBuffer(),
                await sharp(image).extract({ left: 0, top: best.row, width: info.width, height: info.height - best.row }).toBuffer(),
            ]; // 只在连线留白处拆列；所有像素均保留，不改变节点或连接。
        };
        const leftParts = await splitPanel(left.data);
        const rightParts = await splitPanel(right.data);
        const panels = [...leftParts, ...rightParts];
        const panelInfo = await Promise.all(panels.map(image => sharp(image).metadata()));
        const gap = 18;
        const padding = 16;
        const header = 38;
        const width = panelInfo.reduce((sum, item) => sum + item.width, 0) + gap * 3 + padding * 2;
        const height = Math.max(...panelInfo.map(item => item.height)) + header + padding;
        const title = text => sharp({ text: { text, font: 'Arial 17', rgba: true } }).png().toBuffer();
        const overlays = [];
        const captions = ['PyTorch FX: 1/2', 'PyTorch FX: 2/2', 'Netron: 1/2', 'Netron: 2/2'];
        let x = padding;
        for (let index = 0; index < panels.length; index++) {
            const heading = await title(captions[index]);
            const headingInfo = await sharp(heading).metadata();
            overlays.push({ input: heading, left: x + Math.round((panelInfo[index].width - headingInfo.width) / 2), top: 8 });
            overlays.push({ input: panels[index], left: x, top: header });
            x += panelInfo[index].width + gap;
        }
        await sharp({ create: { width, height, channels: 3, background: '#ffffff' } })
            .composite(overlays).png().toFile(path.join(folder, 'fig_02_06_01_PyTorch与ONNX对照.png'));
        console.log(JSON.stringify({ nodeLabels: checks, size: [width, height] }));
    } finally {
        await browser.close();
    }
})();
