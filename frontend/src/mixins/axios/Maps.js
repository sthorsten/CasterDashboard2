import axios from "axios";

export const Maps = {
    data() {
        return {
            maps: null,
            mapsLoaded: null,
        }
    },
    computed: {
        mapImgURLs() {
            let urls = []
            this.maps.forEach(e => {
                urls.push(require('@/assets/img/maps/' + e.id + ".webp"))
            })
            return urls
        },
    },
    methods: {
        getMaps() {
            axios.get(`${this.$store.state.backendURL}/api/core/map/`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.maps = response.data
                this.mapsLoaded = true
            })
        }
    }
}