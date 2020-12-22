<template>
    <div class="wrapper">
        <Navbar></Navbar>
        <!--
        <Sidebar></Sidebar>-->
        <div class="bg-gray-900">

            <b-row class="m-0 p-0 main-content-wrapper">

                <b-col lg="3" xl="2" class="d-none d-lg-block p-0">
                    <Sidebar/>
                </b-col>

                <b-col cols="12" lg="9" xl="10">

                    <div class="content-header">
                        <b-row>
                            <b-col>
                                <h1 class="text-white mt-2 ml-2" style="font-weight: 400">
                                    <template v-if="title_icon">
                                        <i class="mr-2 fa fa-lg" :class="title_icon"></i>
                                    </template>
                                    {{ title }}
                                </h1>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col>
                                <b-breadcrumb class="ml-2" style="margin-top: 0.5rem !important;">
                                    <b-breadcrumb-item active>
                                        <i class="fa fas fa-chevron-circle-right"></i>
                                    </b-breadcrumb-item>
                                    <b-breadcrumb-item active v-for="elem in bc_path" :key="elem.index">
                                        <span>{{ elem }}</span>
                                    </b-breadcrumb-item>
                                </b-breadcrumb>
                            </b-col>
                        </b-row>
                    </div>

                    <div class="content m-2">
                        <slot></slot>
                    </div>

                </b-col>
            </b-row>

        </div>
        <Footer></Footer>
    </div>
</template>

<script>
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import Sidebar from "@/components/layout/Sidebar";

export default {
    name: "BaseLayout",
    props: ['title', 'title_icon', 'bc_path'],
    components: {
        Navbar, Footer, Sidebar
    },

}
</script>

<style scoped>
    .main-content-wrapper{
        min-height: calc(100vh - (38px + 1rem) - (24px + 2rem) - 1px);
    }
</style>