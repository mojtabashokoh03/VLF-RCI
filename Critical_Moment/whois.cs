using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Critical_Moment
{
    class whois
    {
    }


    public partial class Temperatureswhois
    {
        [JsonProperty("WhoisRecord")]
        public WhoisRecord WhoisRecord { get; set; }
    }

    public partial class WhoisRecord
    {
        [JsonProperty("domainName")]
        public string DomainName { get; set; }

        [JsonProperty("parseCode")]
        public long ParseCode { get; set; }

        [JsonProperty("audit")]
        public Audit Audit { get; set; }

        [JsonProperty("registryData")]
        public RegistryData RegistryData { get; set; }

        [JsonProperty("contactEmail")]
        public string ContactEmail { get; set; }

        [JsonProperty("domainNameExt")]
        public string DomainNameExt { get; set; }
    }

    public partial class Audit
    {
        [JsonProperty("createdDate")]
        public string CreatedDate { get; set; }

        [JsonProperty("updatedDate")]
        public string UpdatedDate { get; set; }
    }

    public partial class RegistryData
    {
        [JsonProperty("updatedDate")]
        public DateTimeOffset UpdatedDate { get; set; }

        [JsonProperty("expiresDate")]
        public DateTimeOffset ExpiresDate { get; set; }

        [JsonProperty("registrant")]
        public AdministrativeContact Registrant { get; set; }

        [JsonProperty("administrativeContact")]
        public AdministrativeContact AdministrativeContact { get; set; }

        [JsonProperty("billingContact")]
        public Contact BillingContact { get; set; }

        [JsonProperty("technicalContact")]
        public Contact TechnicalContact { get; set; }

        [JsonProperty("domainName")]
        public string DomainName { get; set; }

        [JsonProperty("nameServers")]
        public NameServers NameServers { get; set; }

        [JsonProperty("rawText")]
        public string RawText { get; set; }

        [JsonProperty("parseCode")]
        public long ParseCode { get; set; }

        [JsonProperty("header")]
        public string Header { get; set; }

        [JsonProperty("strippedText")]
        public string StrippedText { get; set; }

        [JsonProperty("audit")]
        public Audit Audit { get; set; }

        [JsonProperty("updatedDateNormalized")]
        public string UpdatedDateNormalized { get; set; }

        [JsonProperty("expiresDateNormalized")]
        public string ExpiresDateNormalized { get; set; }

        [JsonProperty("whoisServer")]
        public string WhoisServer { get; set; }
    }

    public partial class AdministrativeContact
    {
        [JsonProperty("organization", NullValueHandling = NullValueHandling.Ignore)]
        public string Organization { get; set; }

        [JsonProperty("street1")]
        public string Street1 { get; set; }

        [JsonProperty("city")]
        public string City { get; set; }

        [JsonProperty("state")]
        public string State { get; set; }

        [JsonProperty("country")]
        public string Country { get; set; }

        [JsonProperty("countryCode", NullValueHandling = NullValueHandling.Ignore)]
        public string CountryCode { get; set; }

        [JsonProperty("email")]
        public string Email { get; set; }

        [JsonProperty("telephone")]
        public string Telephone { get; set; }

        [JsonProperty("fax")]
        public string Fax { get; set; }

        [JsonProperty("rawText")]
        public string RawText { get; set; }

        [JsonProperty("unparsable")]
        public string Unparsable { get; set; }

        [JsonProperty("name", NullValueHandling = NullValueHandling.Ignore)]
        public string Name { get; set; }
    }

    public partial class Contact
    {
        [JsonProperty("organization")]
        public string Organization { get; set; }

        [JsonProperty("country")]
        public string Country { get; set; }

        [JsonProperty("countryCode")]
        public string CountryCode { get; set; }

        [JsonProperty("email")]
        public string Email { get; set; }

        [JsonProperty("rawText")]
        public string RawText { get; set; }
    }

    public partial class NameServers
    {
        [JsonProperty("rawText")]
        public string RawText { get; set; }

        [JsonProperty("hostNames")]
        public string[] HostNames { get; set; }

        [JsonProperty("ips")]
        public object[] Ips { get; set; }
    }


}
