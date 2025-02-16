import HtmlWebpackPlugin from "html-webpack-plugin";
import CopyPlugin from "copy-webpack-plugin";
import path from 'path';
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default {
    mode: 'production',
    entry: {
        contentScript: './src/content/index.js',
        background: './src/background/index.js',
        react: './src/react/index.jsx'
    },
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: '[name].js',
        clean: true
    },
    resolve: {
        modules: [path.resolve(__dirname, 'node_modules'), 'node_modules'],
        extensions: ['.js', '.jsx']
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './src/index.html'
        }),
        new CopyPlugin({
            patterns: [
                { from: path.resolve(__dirname, 'src/popup.html'), to: path.resolve(__dirname, 'dist') }, // ✅ Copy popup.html
                { from: path.resolve(__dirname, 'src/styles/popup.css'), to: path.resolve(__dirname, 'dist/styles') }, // ✅ Copy popup.css
                { 
                    from: path.resolve(__dirname, 'manifest.json'), 
                    to: path.resolve(__dirname, 'dist'),
                    transform(content) {
                        const manifest= JSON.parse(content.toString());
                        manifest.action.default_popup = "popup.html";
                        return JSON.stringify(manifest, null, 2);
                    } } // ✅ Copy manifest.json
            ]
        })
    ],
    
    module: {
        rules: [
            {
                test: /\.js$|jsx/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: [
                            '@babel/preset-env',
                            ['@babel/preset-react', {'runtime': 'automatic'}]
                        ]
                    }
                }
            }
        ]
    }
}
