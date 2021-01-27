import VuexPersistence from 'vuex-persist'

export default ({ store }) => {
    new VuexPersistence({
        storage: sessionStorage
    }).plugin(store);
}
