export default function ({ $axios }, inject) {
    // Create a custom axios instance
    const localAxios = $axios.create()

    // Set baseURL to empty
    localAxios.setBaseURL('')

    inject('localAxios', localAxios)
}
