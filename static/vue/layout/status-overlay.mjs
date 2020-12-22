const template = `
    <div class="overlay dark" style="height: 400px">
        <div class="row w-100 text-center">
            <div class="col-12">
                <template v-if="type === 'loading'">
                    <div class="spinner-border" role="status">
                    </div>                    
                </template>
                <template v-if="type === 'icon' && icon != null">
                    <i :class="icon"></i>
                </template>
            
            </div>
            <div class="col-12">
                <div class="text-bold pt-2">{{ text }}</div>
            </div>
        </div>
    </div>
`


export const StatusOverlay = {
    name: "StatusOverlay",
    props: {
        type: String,
        text: String,
        icon: String,
    },
    template: template
}