<template>
  <div>
    <Notification class="my-1" position="top center" />
    <v-dialog persistent v-model="dialog" max-width="800">
      <v-card flat :class="$style.dialog">
        <template v-if="!help">
          <v-card-title :class="$style.title">
            Buy {{ testSeries.name }}
            <v-spacer />
            <v-btn round outline color="primary" v-on:click="toggleHelp()"
              >Help</v-btn
            >
            <v-btn flat icon color="error" @click="$emit('close')">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>

          <v-card-text :class="$style.subheading">
            Make a payment of &#8377;{{ testSeries.price }} using one of these
            methods and submit transaction id and receipt after successful
            payment.The demo receipts are shown in help.
          </v-card-text>
          <v-layout row wrap>
            <v-flex xs12 md6>
              <div :class="$style.subheading">
                Scan and Pay Using Google Pay
              </div>
              <v-img
                :src="require(`@/assets/images/payment/PankajQRcode.jpg`)"
                class="ma-auto"
                width="300px"
              />
            </v-flex>
            <v-flex xs12 md6>
              <div :class="$style.subheading">Bank Account Details</div>
              Account No: 37953774240<br />
              Acoount Holder Name: Pankaj Kumar Jha<br />
              IFSC Code: SBIN0011445
              <v-divider class="my-3" />
              <div :class="$style.subheading">UPI Details</div>
              UPI ID: pk20pankajjha@oksbi<br />
              Phone Number: +918887864114 <br />
              (For Google Pay and PhonePe)
            </v-flex>
            <v-flex xs12>
              <form enctype="multipart/form-data">
                <v-text-field v-model="transaction_id" label="Transaction Id" />
                <input
                  type="file"
                  v-show="false"
                  ref="receipt"
                  v-on:change="handleFileUpload()"
                />
                <div class="text-xs-left">
                  <v-btn
                    round
                    outline
                    small
                    color="primary"
                    @click="$refs.receipt.click()"
                  >
                    <label for="receipt">choose receipt</label>
                  </v-btn>
                  <span> {{ receipt.name }}</span>
                </div>
              </form>
            </v-flex>
          </v-layout>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn flat color="error" @click="$emit('close')">cancel</v-btn>
            <v-btn color="primary" @click="submit">
              submit
            </v-btn>
          </v-card-actions>
        </template>

        <template v-else>
          <v-card-title :class="$style.title">
            The receipts for various payment methods will look like these.
            <br />
            <v-spacer />
            <v-btn outline round color="primary" v-on:click="toggleHelp()">
              back
            </v-btn>
            <div>
              <b
                >Note: The transaction id is encircled
                <span class="red--text">red</span>.</b
              >
            </div>
          </v-card-title>
          <v-layout justify-center>
            <v-flex
              v-for="card in cards"
              :key="card.title"
              v-bind="{ [`xs${card.flex}`]: true }"
              class="mx-2"
            >
              <h3>{{ card.title }}</h3>
              Receipt <v-img :src="card.receipt_src" />
            </v-flex>
          </v-layout>
        </template>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  props: ["dialog", "testSeries"],
  data() {
    return {
      help: false,
      transaction_id: "",
      receipt: "",
      cards: [
        {
          title: "Google Pay",
          receipt_src: require(`@/assets/images/payment/gpay.jpg`),
          flex: 4
        },
        {
          title: "PhonePe",
          receipt_src: require(`@/assets/images/payment/phonepe.jpg`),
          flex: 4
        },
        {
          title: "Netbanking",
          receipt_src: require(`@/assets/images/payment/netbanking.jpg`),
          flex: 4
        }
      ]
    };
  },
  methods: {
    handleFileUpload() {
      this.receipt = this.$refs.receipt.files[0];
    },
    toggleHelp() {
      this.help = !this.help;
    },
    submit() {
      if (!this.transaction_id) {
        this.$notify({
          type: "warning",
          title: "Warning",
          text: "Enter transaction ID."
        });
        return;
      } else if (!this.receipt) {
        this.$notify({
          type: "warning",
          title: "No file chosen!",
          text: "Please chose a receipt image or pdf."
        });
        return;
      } else if (this.receipt.size > 1024 * 1024) {
        this.$notify({
          type: "warning",
          title: "Size limit exceeded!",
          text: "File size must be less than 1MB."
        });
        return;
      } else {
        let formData = new FormData();
        formData.append("test_series", this.testSeries.id);
        formData.append("amount", this.testSeries.price);
        formData.append("transaction_id", this.transaction_id);
        formData.append("receipt", this.receipt, this.receipt.name);
        this.$store.dispatch("payments/create", formData);
        this.$emit("close");
      }
    }
  }
};
</script>

<style module lang="stylus">
.dialog {
  font-family: 'Product Sans Light', Roboto, Arial, sans-serif;
  padding: 20px;
  border-radius: 8px;

  .title {
    font-size: 1.575rem;
    line-height: 1.75rem;
    color: #5e5766;
  }
  .subheading{
    font-size: 1.375rem;
  }
}
</style>
