import HtmlWebpackPlugin from "html-webpack-plugin";
import CopyPlugin from "copy-webpack-plugin";
import path from 'path';

export default {
    mode: 'production',
    entry: {
        contentScript: './src/content/index.js',
        background: './src/background/index.js',
        react: './src/react/index.jsx'
    },
    output: {
        path: path.resolve('dist'),
        filename: '[name].js',
        clean: true
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './src/index.html'
        }),
        new CopyPlugin({
            patterns: [{
                from: path.resolve('manifest.json'),
                
            }]
        })
    ]
}