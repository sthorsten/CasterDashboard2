export const state = () => ({
    pageTitle: "",
    pageTitleIcon: null,
    breadcrumbPath: [],
    version: "?"
})

export const mutations = {
    setPageTitle(state, title){
        state.pageTitle = title
    },

    setPageTitleIcon(state, icon){
        state.pageTitleIcon = icon
    },

    setBreadcrumbPath(state, bcPath){
        state.breadcrumbPath = bcPath
    },

    setVersion(state, version){
        state.version = version
    }

}
