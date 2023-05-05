<template>
  <v-container class="text-center  ma-0 pa-0">
    <v-row class="text-center ">
      <v-col cols="12">
        <div class="videobox">
          <RecorderView 
            :video-source="videoSource"
            @error="onError"
            @cameras="onCameras"
            @video-live="onVideoLive"
            @view-change="onViewChange"
            @new-recording="onNewRecording"
            @delete-recording="onDeleteRecording"
            @player-loaded="onPlayerLoaded"
            ref="recorder"
            :videoTypes="videoTypes"
            :recorderMode="recorderMode"
          />
        </div>
        <v-select
          v-if="videoSource == null"
          v-show="view == 'video'"
          :items="videoSourceList"
          :return-object="true"
          v-model="videoSource"
          label="Select video input"
        />
        <div
          v-if="videoSource"
          align="right"
          background-color="black"
          class="grey--text videobox"
        >
          {{ videoSource.text }}
          <v-icon @click="videoClose" color="grey">mdi-close-circle</v-icon>
        </div>
        
        <v-row v-show="view == 'videoPlayer'" class="text-center  mt-3 pt-0">
          <v-col align="center">
            <v-btn class="mx-2" @click="downloadRecording" fab mdi-icon x-small light
              ><v-icon x-large>mdi-cloud-upload</v-icon></v-btn
            >
            <v-btn class="mx-2" @click="deleteRecording" fab mdi-icon x-small light
              ><v-icon x-large color="red">mdi-delete-circle</v-icon></v-btn
            >
          </v-col>
        </v-row>
        
        <v-row v-show="view == 'video' && videoSource != null">
          <v-col align="center">
            <v-btn v-show="controls == 'liveVideo'" class="mx-2" @click="videoRecord" fab mdi-icon x-small light
              ><v-icon x-large color="red">mdi-record-circle</v-icon></v-btn
            >
            <v-btn v-show="controls == 'recordingVideo'" class="mx-2" @click="videoStopRecording" fab mdi-icon x-small light
              ><v-icon x-large color="red">mdi-stop-circle</v-icon></v-btn
            >
          </v-col>
        </v-row>

      </v-col>
    </v-row>
  </v-container>
</template>

<script>
/**
 * For Hot reload load the `*.vue` files from the parent `/src/` directly.
 */
// import { RecorderView } from './RecorderView.vue';
// import { Multicorder } from "../../../src/lib-components/index.js";

export default {
  name: "RecorderUI",
  components: {
    RecorderView: () => import('./RecorderView.vue')
  },
  props: {
    videoTypes: {
      type: Array,
      default: () => {
        return ["camera", "screen"];
      },
    },
    recorderMode: {
      type: String,
      default: "single",
    },
  },
  data() {
    return {
      controls: null,
      videoSource: null,
      videoSourceList: [],
      isPaused: false,
      isPlayerPaused: false,
      isMuted: true,
      isPlayerMuted: true,
      view: "video",
      recordings: [], // local sparsed list of recording data
    };
  },
  methods: {
    onError(error) {
      console.log("Error emitted", error);
    },
    onCameras(cameras) {
      console.log("Available cameras", cameras);
      /**
       * We are implementing a `recorder` with camera and screen support.
       * We need to create a list that groups the items for a `v-select` component.
       * We use the `listFromCameras` helper function provided by the component.
       * The Multicorder component maintains a list of `cameras` if we need them independently.
       */
      this.videoSourceList = this.$refs.recorder.listFromCameras(cameras);
    },
    onVideoLive() {
      this.controls = "liveVideo";
    },
    onViewChange(view) {
      this.view = view;
    },
    onNewRecording(recording) {
      this.recordings.push(recording);
      if (this.recorderMode == "single") {
        // Load the video into the player and force disposition
        // this.view = "videoPlayer";
        this.loadRecording(0);
      }
    },
    onDeleteRecording(index) {
      this.recordings.splice(index, 1);
      if (this.recorderMode == "single") {
        this.controls = "liveVideo"  
      }
    },
    onPlayerLoaded() {
      //this.playRecording();
    },
    videoRecord() {
      this.controls = "recordingVideo";
      this.$refs.recorder.startVideoRecording();
    },
    videoSnapshot(fromView) {
      this.$refs.recorder.videoSnapshot(fromView);
    },
    videoClose() {
      this.$refs.recorder.stopVideo();
      this.view = "video";
      this.controls = "liveVideo";
      this.videoSource = null;
    },
    videoStopRecording() {
      this.$refs.recorder.stopRecording();
      // resume the video, minus recording
      console.log(this.$refs.recorder);
      this.resume();
    },
    resume() {
      this.isPaused = false;
      this.$refs.recorder.resume();
    },
    pause() {
      this.isPaused = true;
      this.$refs.recorder.pause();
    },
    closeSnapshot() {
      this.$refs.recorder.closeSnapshot();
    },
    snapshotDownload() {
      this.$refs.recorder.downloadSnapshot();
    },
    downloadRecording(index) {
      if(this.recorderMode === 'single') {
        index = 0;
      }
      this.$refs.recorder.downloadRecording(index);
    },
    deleteRecording(index) {
      if(this.recorderMode === 'single') {
        index = 0;
      }
      this.$refs.recorder.deleteRecording(index);
    },
    async loadRecording(index) {
      await this.$refs.recorder.loadRecording(index);
    },
    playRecording() {
      this.isPlayerPaused = false;
      this.$refs.recorder.playRecording();
    },
    pausePlayer() {
      this.isPlayerPaused = true;
      this.$refs.recorder.pausePlayer();
    },
    resumePlayer() {
      this.isPlayerPaused = false;
      this.$refs.recorder.resumePlayer();
    },
    deletePlayerRecording() {
      this.$refs.recorder.deletePlayerRecording();
    },
    closePlayer() {
      this.$refs.recorder.closePlayer();
    },
    toggleMuted() {
      this.isMuted = !this.isMuted;
    },
    togglePlayerMuted() {
      this.isPlayerMuted = !this.isPlayerMuted;
    },
  },
};
</script>

<style scoped>
.videobox {
  background-color: black;
}
</style>
