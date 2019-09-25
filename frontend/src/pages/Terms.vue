<template>
  <StandardLayout>
    <v-flex xs12>
      <v-layout column>
        <v-card :class="[$style.card, 'elevation-0']">
          <v-card-title class="title">
            Terms And Conditions
          </v-card-title>
          <v-card-text class="text-xs-left">
            Please read the terms carefully before using this website. All
            rights reserved by the Company, including changing these Terms and
            Conditions with no prior notice, and you are solely responsible to
            review these Terms and Conditions regularly.

            <p>
              <strong> DESCRIPTIONS:</strong><br />
              The Company has tried to describe its products as accurate as
              possible. However, it doesn't mean all the product descriptions
              and other content are accurate, complete, reliable, current or
              error-free. You are supposed to contact eTests via Contact details
              mentioned in website, if the product you purchased on this site is
              not substantially as described.
              <br />
              <strong>PRIVACY POLICY:</strong><br />
              The Personal information, email that submitted while registering
              to the site, will NOT be distributed, shared with any other
              third-parties. We only use this data for our information, for
              research, to improve our services and for contacting you purposes.
              Registration to the website is mandatory for attempting or
              purchasing any test or Question banks. Registration into the site
              is purely of user’s interest. www.etests.co.in reserves the right
              to change this policy at any time.
              <br />
              <strong>ANTI-SPAM POLICY :</strong><br />
              www.etests.in is against in sending spam, unsolicited emails. You
              should not use our service and you are not authorized to use our
              referral or email services, for your personal or commercial
              purposes. By usage of this service you agreed that to our
              policies. Violating these policies in any manner subject to
              violation of respected laws and necessary action will be initiated
              against the defaulters.
              <br />
              <strong>COPYRIGHT :</strong><br />
              All content contained by this site, including text, graphics,
              logos, button icons, images, audio clips, digital downloads, and
              data compilations is the exclusive property of the Company or its
              content suppliers and is under protection by both domestic and
              international Copyright Laws. The compilation of all content on
              this site is exclusive property of the Company and is protected by
              both domestic and international copyright laws.
              <br />
              <strong>LICENSE AND SITE ACCESS :</strong><br />
              The Company grants you a limited time license to access this site,
              to purchase the products and use the services offered by this site
              only for personal use. The actions listed below are strictly
              prohibited unless you receive the prior written consent of the
              Company: Downloading (other than page caching), Copying,
              Modifying, Reproducing, Duplicating, or any Derivative use of this
              site or its contents; any Collection or use of any product
              listings, Descriptions, or Prices; any use of Data Mining, Robots,
              or Similar Data gathering and Extraction Devices; Using or framing
              any Trademark, Logo, or other Proprietary Information (including
              images, text, page layout, or form) of the Company; Using Meta
              Tags or any other "hidden text" utilizing the Company's name or
              trademarks; Any exploitation of this site or its contents for any
              commercial purpose.<br />

              <strong>FRAUDULENT ACTIVITY :</strong><br />
              You agree to cooperate fully with the Company in any investigation
              by the Company or its agents regarding fraudulent or improper
              activity related to the use of this site and its resource,
              including, but not limited to, fraudulent charge backs and false
              claims regarding to non-receipt of products.
              <br />
              <strong>THIRD-PARTY SITES:</strong><br />
              This site may also contain links or pointers to Internet sites
              owned and operated by third parties. The Company does not operate
              or control any information, products or services appearing on or
              offered through these third-party sites, is not responsible for
              examining or evaluating these third-party sites and does not
              assume any responsibility or liability for any actions, products,
              or content related to these third-party sites.
              <br />
              <strong>REVIEWS, COMMENTS AND OTHER CONTENT:</strong><br />
              Visitors may post reviews, comments, or some other related
              content, but the visitors should acknowledge that the content is
              not illegal, obscene, threatening, defamatory, invasive of
              privacy, infringing on intellectual property rights of or
              otherwise injurious to third parties, and does not contain
              software viruses, political campaigning, commercial solicitation,
              chain letters, mass mailings, or any form of "spam." You may not
              use an invalid e-mail address, impersonate any person or entity,
              or otherwise mislead as to the origin of any such content. The
              Company reserves the right to delete or edit such content.
              However, the company does not review posted content regularly.
              When you post the content, you are supposed to grant the Company a
              nonexclusive, royalty-free, perpetual, irrevocable, and fully
              sub-licensable right to use, reproduce, modify, adapt, publish,
              translate, create derivative works from, distribute, and display
              such content throughout the world in any media. Besides, you grant
              the Company and its sub-licensees the right to use the name that
              you submit in connection with such content, if they choose. You
              represent and warrant that you own all of the rights to such
              content; that such content is accurate; that use of such content
              does not infringe on the rights of, or cause injury to, any person
              or entity; and that you indemnify the Company for all claims
              resulting from such content. The Company reserves the right but
              not the obligation to monitor, edit or remove any activity or
              content on this site. The Company takes no responsibility and
              assumes no liability for any content posted on this site by you or
              any third party.
              <br />
              <strong>SERVICE CONDITIONS</strong><br />
              Our all functionality are available on demo. It shall be your
              responsibility to go for all the terms & conditions. We are not
              responsible to ensure that any services or information available
              through eTests meet your specific requirement.
              <br />
              <strong>SUPPORT CONDITIONS</strong><br />
              We provide 24*7 Online Support through Phone(whatsapp or call) or
              Email.
              <br />
              <strong>JURISDICTION</strong><br />
              All disputes are subject to Varanasi jurisdiction only.
              <br />

              <strong>TERMS & CONDITIONS</strong><br />
              If your visit or use of this website, it means that you accept
              these terms and conditions and acknowledge that these terms and
              conditions can work as a binding agreement between you and the
              Company. Please read the terms carefully before using this
              website. All rights reserved by the Company, including changing
              these Terms and Conditions with no prior notice, and you are
              solely responsible to review these Terms and Conditions regularly.
              <br />
            </p>
          </v-card-text>
        </v-card>
      </v-layout>
    </v-flex>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";

export default {
  components: {
    StandardLayout
  }
};
</script>
<style module lang="stylus">
.card{
  padding: 10px 20px;
  width: 100%;
  border-radius: 8px;
  font: "Montserrat Light";
  margin-bottom: 12px;
}
p{
font-family: "Montserrat Light";
}
</style>
