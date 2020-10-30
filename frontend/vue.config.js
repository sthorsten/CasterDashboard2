module.exports = {
    pluginOptions: {
        resolve: {
            alias: {
                vue$: 'vue/dist/vue.esm.js'
            },
        },
        i18n: {
            locale: 'en',
            fallbackLocale: 'en',
            localeDir: 'locales',
            enableInSFC: true
        }
    }
}
