<template>
  <div>
    <div>
      <template>
        <v-simple-table fixed-header id="header">
          <template v-slot:default>
            <thead>
              <tr>
                <th class="text-left">User Name</th>
                <th class="text-left">Nitrogen</th>
                <th class="text-left">Phosphorus</th>
                <th class="text-left">Potassium</th>
                <th class="text-left">Temperature</th>
                <th class="text-left">Humidity</th>
                <th class="text-left">Soil Moisture</th>
                <th class="text-left">Soil Type</th>
                <th class="text-left">Crop Type</th>
                <th class="text-left">Recommend Fertilizer</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="value in datas" :key="value.id">
                <td>{{ value.user_name }}</td>
                <td>{{ value.nitrogen }}</td>
                <td>{{ value.phosphorus }}</td>
                <td>{{ value.potassium }}</td>
                <td>{{ value.temperature }}</td>
                <td>{{ value.humidity }}</td>
                <td>{{ value.soil_moisture }}</td>
                <td>{{ value.soil_type }}</td>
                <td>{{ value.crop_type }}</td>
                <td>{{ value.result }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </template>
    </div>

    <v-card :loading="loading" class="mx-auto my-12" max-width="374">
      <v-container class="justify-center">
        <template slot="progress">
          <v-progress-linear
            color="primary"
            height="10"
            indeterminate
          ></v-progress-linear>
        </template>

        <v-card-title class="justify-center">Crop Recommendation</v-card-title>

        <v-card-text>
          <template>
            <ValidationObserver ref="observer" v-slot="{ invalid }">
              <form @submit.prevent="Submit">
                <ValidationProvider name="Nitrogen" rules="required|max:9">
                  <v-text-field
                    v-model="nitrogen"
                    type="number"
                    :counter="9"
                    label="Nitrogen"
                    required
                    dense
                    filled
                    hide-details="auto"
                  />
                </ValidationProvider>

                <ValidationProvider name="Phosphorus" rules="required|max:9">
                  <v-text-field
                    v-model="phosphorus"
                    type="number"
                    :counter="9"
                    label="Phosphorus"
                    required
                    dense
                    filled
                    hide-details="auto"
                  />
                </ValidationProvider>

                <ValidationProvider name="Potassium" rules="required|max:9">
                  <v-text-field
                    v-model="potassium"
                    type="number"
                    :counter="9"
                    label="Potassium"
                    required
                    dense
                    filled
                    hide-details="auto"
                  />
                </ValidationProvider>

                <ValidationProvider name="Temperature" rules="required|max:9">
                  <v-text-field
                    v-model="temperature"
                    type="number"
                    :counter="9"
                    label="Temperature"
                    required
                    dense
                    filled
                    hide-details="auto"
                  />
                </ValidationProvider>

                <ValidationProvider name="Humidity" rules="required|max:9">
                  <v-text-field
                    v-model="humidity"
                    type="number"
                    :counter="9"
                    label="Humidity"
                    required
                    dense
                    filled
                    hide-details="auto"
                  />
                </ValidationProvider>

                <ValidationProvider name="Soil Moisture" rules="required|max:9">
                  <v-text-field
                    v-model="soil_moisture"
                    type="number"
                    :counter="9"
                    label="Soil Moisture"
                    required
                    dense
                    filled
                    hide-details="auto"
                  />
                </ValidationProvider>

                <ValidationProvider name="Soil Type" rules="required|max:9">
                  <v-select
                    :items="soil_item"
                    v-model="soil_type"
                    :counter="9"
                    label="Soil Type"
                    required
                    dense
                    filled
                  ></v-select>
                </ValidationProvider>

                <ValidationProvider name="Crop Type" rules="required|max:9">
                  <v-select
                    :items="crop_item"
                    v-model="crop_type"
                    :counter="9"
                    label="Crop Type"
                    required
                    dense
                    filled
                  ></v-select>
                </ValidationProvider>
                <div>
                  <v-spacer></v-spacer>
                  <v-btn class="ma-4" text @click="Submit" :disabled="invalid">
                    Submit
                  </v-btn>
                </div>
              </form>
            </ValidationObserver>
          </template>
        </v-card-text>
      </v-container>
    </v-card>
  </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import { required, email, min, max } from "vee-validate/dist/rules";
import { extend, setInteractionMode } from "vee-validate";

setInteractionMode("eager");

extend("required", {
  ...required,
  message: "{_field_} can not be empty",
});

extend("min", {
  ...min,
  message: "{_field_} may not be less than {length} characters",
});

extend("max", {
  ...max,
  message: "{_field_} may not be more than {length} characters",
});

extend("email", {
  ...email,
  message: "Email must be valid",
});

export default {
  data: () => ({
    datas: "",
    nitrogen: 0,
    phosphorus: 0,
    potassium: 0,
    temperature: 0,
    humidity: 0,
    soil_moisture: 0,
    soil_type: "",
    crop_type: "",
    soil_item: ["Sandy", "Loamy", "Black", "Red", "Clayey"],
    crop_item: [
      "Maize",
      "Sugarcane",
      "Cotton",
      "Tobacco",
      "Paddy",
      "Barley",
      "Wheat",
      "Millets",
      "Oil seeds",
      "Pulses",
    ],
    token: Vue.$cookies.get("token"),
  }),

  mounted() {
    this.Get();
  },

  methods: {
    Submit() {
      this.$refs.observer.validate().then((success) => {
        if (!success) {
          return;
        }

        axios({
          method: "POST",
          url: "http://127.0.0.1:8000/fertilizer/",
          data: {
            nitrogen: this.nitrogen,
            phosphorus: this.phosphorus,
            potassium: this.potassium,
            temperature: this.temperature,
            humidity: this.humidity,
            soil_moisture: this.soil_moisture,
            soil_type: this.soil_type,
            crop_type: this.crop_type,
          },
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `token ${this.token}`,
          },
        })
          .then((res) => {
            console.log(res);
            alert("Car Mileage Predicted Successfully!");
            window.location.reload();
          })
          .catch((error) => {
            alert(error.response.data);
            this.errored = true;
          });

        this.loading = true;
        setTimeout(() => (this.loading = false), 2000);
      });
    },

    Get() {
      axios({
        method: "GET",
        url: "http://127.0.0.1:8000/fertilizer/",
        data: JSON.stringify({}),
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
          Authorization: `token ${this.token}`,
        },
      })
        .then((res) => {
          this.datas = res.data;
          console.log(this.datas);
        })
        .catch((error) => {
          alert(error.response.data);
          this.errored = true;
        });
    },
  },
};
</script>

<style></style>
