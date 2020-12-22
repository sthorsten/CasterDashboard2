const template = `
    <div class="card mb-3" :class="[colorClass, {'card-outline-all' : outline }]">
        <div class="card-body bg-gray-800 text-white">
            <h5 class="card-title card-title-upper">{{ title }}</h5>
            <template v-if="divider">
                <br>
                <div class="card-divider"></div>
            </template>
            <template v-else>
                <br><br>
            </template>
            <slot name="card-body"></slot>
        </div>
        <template v-if="footer">
            <div class="card-footer bg-gray-700">
                <slot name="card-footer"></slot>
            </div>        
        </template>
    </div>
`

export const Card = {
    name: "Card",
    props: {
        title: String,
        color: String,
        outline: Boolean,
        divider: Boolean,
        footer: Boolean,
    },
    computed: {
        colorClass() {
            return "card-" + this.color
        }
    },
    template: template
}