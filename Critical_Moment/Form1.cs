using Freezer.Core;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Configuration;
using System.Data;
using System.Data.SqlClient;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Mail;
using System.Net.Sockets;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using System.Net.Http;
using HtmlAgilityPack;

namespace Critical_Moment
{

    public partial class Form1 : Form
    {

        static IWebDriver driver;
        string useragentall = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.38 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.38";
        string whoamirun = "Iran";
        CancellationTokenSource tokenSource1 = new CancellationTokenSource();
        Task task1;
        bool start = false;
        CancellationTokenSource tokenSource2 = new CancellationTokenSource();
        Task task2;
        bool start2 = false;
        CancellationTokenSource tokenSource3 = new CancellationTokenSource();
        Task task3;
        bool start3 = false;
        CancellationTokenSource tokenSource4 = new CancellationTokenSource();
        Task task4;
        bool start4 = false;
        CancellationTokenSource tokenSource5 = new CancellationTokenSource();
        Task task5;
        bool start5 = false;
        CancellationTokenSource tokenSource6 = new CancellationTokenSource();
        Task task6;
        bool start6 = false;
        CancellationTokenSource tokenSource7 = new CancellationTokenSource();
        Task task7;
        bool start7 = false;
        CancellationTokenSource tokenSource8 = new CancellationTokenSource();
        Task task8;
        bool start8 = false;

        CancellationTokenSource tokenSource9 = new CancellationTokenSource();
        Task task9;
        bool start9 = false;
        public Form1()
        {
            InitializeComponent();
            /*
            var htmlDoc = new HtmlAgilityPack.HtmlDocument();
            htmlDoc.LoadHtml("<a></a>");

            var htmlNodes = htmlDoc.DocumentNode.SelectNodes("//body/h1");

            foreach (var node in htmlNodes)
            {
                Console.WriteLine(node.InnerHtml);
            }
            foreach (HtmlNode link in htmlDoc.DocumentNode.SelectNodes("//a[@href]"))
            {

            }*/
        }

        private void button1_Click(object sender, EventArgs e)
        {

            if (!start)
            {
                tokenSource1 = new CancellationTokenSource();
                CancellationToken ct = tokenSource1.Token;
                start = true;
                task1 = Task.Run(() => startwork(), tokenSource1.Token);
                button1.Enabled = false;
                button2.Enabled = true;
            }


        }
        private void button2_Click(object sender, EventArgs e)
        {
            if (start)
            {
                tokenSource1.Cancel();
                tokenSource1.Dispose();
                start = false;
                label2.Text = "Stop at " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss");

                button2.Enabled = false;
                button1.Enabled = true;
            }
        }
        public async Task startwork()
        {
            while (start)
            {
                label2.Text = "Start proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task1.Status.ToString();
                await GetResponseAsync();

                label2.Text = "Compelet proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " And go to sleep for " + textBox3.Text + " minutes " + task1.Status.ToString();
                await Task.Delay(int.Parse(textBox3.Text) * 1000 * 60);

            }
        }
        public string getdeturl(string url, string idphish)
        {
            try
            {
                string newurl = "";

                ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };
                HttpWebRequest request = (HttpWebRequest)HttpWebRequest.Create("https://phishtank.org/phish_detail.php?phish_id=" + idphish);
                request.UserAgent = useragentall;
                var response = (HttpWebResponse)request.GetResponse();

                Stream stream = response.GetResponseStream();
                StreamReader strReader = new StreamReader(stream);
                string text = strReader.ReadToEnd();
                int start = 0;
                int end = 0;
                start = text.IndexOf(url.Replace("...", ""), end);
                if (start == -1)
                    return "";
                end = text.IndexOf("</b>", start);
                if (end == -1)
                    return "";
                if (end < start)
                    return "";
                try
                {
                    newurl = text.Substring(start, end - start);
                }
                catch
                {

                }
                return newurl;
            }
            catch
            {
                return "";
            }

        }
        public async Task GetResponseAsync()
        {
            try
            {
                
                    listBox1.Items.Clear();

                    listBox1.Items.Add(" Prepare for insert in date of " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss"));
                for (int iter = 0; iter < 3; iter++)
                {
                    ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };
                    HttpWebRequest request;

                    if (iter==0)
                        request = (HttpWebRequest)HttpWebRequest.Create("https://phishtank.org/phish_search.php");
                    else if (iter == 1)
                        request = (HttpWebRequest)HttpWebRequest.Create("https://phishtank.org/phish_search.php?verified=u&active=y");
                    else 
                        request = (HttpWebRequest)HttpWebRequest.Create("https://phishtank.org/phish_search.php?verified=u");
                    request.UserAgent = useragentall;
                    var response = (HttpWebResponse)await Task.Factory.FromAsync<WebResponse>(request.BeginGetResponse, request.EndGetResponse, null);

                    Stream stream = response.GetResponseStream();
                    StreamReader strReader = new StreamReader(stream);
                    string text = await strReader.ReadToEndAsync();
                    StringBuilder stb = new StringBuilder();
                    int start = 0;
                    int end = 0;
                    int nstart = 0;
                    int nend = 0;
                    int leng = 0;
                    string temp = "";
                    string url = "";
                    string idphish = "";
                    string time = "";
                    List<urlph> liph = new List<urlph>();
                    while (true)
                    {
                        start = text.IndexOf("><a href=\"phish_detail.php?phish_id", end);
                        if (start == -1)
                            break;
                        end = text.IndexOf("</span></td><td valign=\"center\" class=\"value\">by", start);
                        if (end == -1)
                            break;
                        if (end < start)
                            break;
                        try
                        {
                            temp = text.Substring(start, end - start);
                            if (temp == "")
                                continue;
                            try
                            {
                                nstart = 0;
                                nend = 0;
                                nstart = temp.IndexOf("<td valign=\"center\" class=\"value\">http", nend);
                                if (start == -1)
                                    break;

                                nend = temp.IndexOf("<br /><span class=\"small\">", nstart);
                                url = temp.Substring(nstart, nend - nstart).Replace("<td valign=\"center\" class=\"value\">", "");
                            }
                            catch { }
                            try
                            {
                                nstart = 0;
                                nend = 0;
                                nstart = temp.IndexOf("><a href=\"phish_detail.php?phish_id=", nend);
                                if (start == -1)
                                    break;
                                nend = temp.IndexOf("\">", nstart);
                                idphish = temp.Substring(nstart, nend - nstart).Replace("><a href=\"phish_detail.php?phish_id=", "");
                            }
                            catch { }
                            try
                            {
                                nstart = 0;
                                nend = 0;
                                nstart = temp.IndexOf("<br /><span class=\"small\">added on ", nend);
                                if (start == -1)
                                    break;
                                leng = temp.Length;
                                time = temp.Substring(nstart, leng - nstart).Replace("<br /><span class=\"small\">added on ", "");
                            }
                            catch { }
                            if (url.Contains("..."))
                            {
                                try
                                {
                                    string tempw = getdeturl(url, idphish);
                                    if (tempw != "")
                                        url = tempw;
                                }
                                catch
                                {

                                }
                            }
                            liph.Add(new urlph { url = url, id = idphish, detail = time });

                        }
                        catch (Exception ex)
                        { listBox1.Items.Add(ex.ToString()); }
                    }
                    Boolean has = false;
                    Boolean hasinsert = false;
                    foreach (var suli in liph)
                    {
                        SqlConnection cnn = new SqlConnection(ConfigurationManager.ConnectionStrings["pliconnectionstring"].ConnectionString);
                        SqlCommand cmd1;
                        SqlDataReader reader;
                        has = false;
                        cnn.Close(); cnn.Open();
                        cmd1 = new SqlCommand("select id from phishdata where idphish =@idphish", cnn);
                        cmd1.Parameters.AddWithValue("@idphish", suli.id);
                        reader = cmd1.ExecuteReader();
                        while (reader.Read())
                        {
                            has = true;
                            break;
                        }
                        cnn.Close();
                        if (!has)
                        {
                            suli.url = suli.url.Replace("&amp;", "&");
                            if (suli.url.Contains("<a href=\"/cdn-cgi/l/email-protection\" class=\"__cf_email__\" data-cfemail=\""))
                                sendmail(suli.id);
                            //    suli.url = Regex.Split(suli.url, "<a href=\"/cdn-cgi/l/email-protection\" class=\"__cf_email__\" data-cfemail=\"")[0];

                            hasinsert = true;
                            cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("insert into phishdata([url],[isphish],[dtime],[idphish],[datecreate] ) values (@url,@isphish,@dtime,@idphish,@datecreate)", cnn);
                            cmd1.Parameters.AddWithValue("@url", suli.url);
                            cmd1.Parameters.AddWithValue("@isphish", -1);
                            cmd1.Parameters.AddWithValue("@dtime", suli.detail);
                            cmd1.Parameters.AddWithValue("@idphish", suli.id);
                            cmd1.Parameters.AddWithValue("@datecreate", DateTime.Now);
                            cmd1.ExecuteNonQuery();
                            cnn.Close();

                            listBox1.Items.Add(suli.url + " " + suli.id + " " + suli.detail);
                        }

                    }
                    if (!hasinsert)
                        listBox1.Items.Add("No new item insert in date " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss"));
                }
            }
            catch (Exception ex)
            {
                listBox1.Items.Add(ex.ToString());
            }
        }

        protected string[] onlinessl(string url)
        {
            string[] ret = { "", "", "", "" };
            try
            {
                Uri u = new Uri(url.Replace("http://", "https://"));
                ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };
                ServicePoint sp = ServicePointManager.FindServicePoint(u);

                string groupName = Guid.NewGuid().ToString();
                HttpWebRequest req = HttpWebRequest.Create(u) as HttpWebRequest;
                req.ConnectionGroupName = groupName;
                if (int.TryParse(textBox5.Text, out int outi))
                    req.Timeout = outi;
                else
                    req.Timeout = 10000;

                using (WebResponse resp = req.GetResponse())
                {
                }
                sp.CloseConnectionGroup(groupName);
                X509Certificate2 x509 = new X509Certificate2(sp.Certificate);
                ret[0] = "1";
                ret[1] = x509.GetEffectiveDateString();
                ret[2] = x509.GetExpirationDateString();
                ret[3] = x509.GetNameInfo(X509NameType.SimpleName, true);


            }
            catch (Exception ex)
            {
                if (url.StartsWith("http://"))
                    ret[0] = "0";
            }
            return ret;
        }

        protected string[] iranwhois(string url)
        {
            string[] ret = { "", "", "", "" };
            int itag = 0;
            url = url.Replace(" ", "").Replace("\\", "/").Replace("http://", "").Replace("https://", "").Split('/')[0].Split('?')[0];


            try
            {


               var request = (HttpWebRequest)HttpWebRequest.Create("http://162.19.186.252/home/index");
                request.Method = "post";
                var postData = "id=" + Uri.EscapeDataString(url);
                var data = Encoding.ASCII.GetBytes(postData);

                request.Method = "POST";
                request.ContentType = "application/x-www-form-urlencoded";
                request.ContentLength = data.Length;
                request.UserAgent = useragentall;

                using (var stream1 = request.GetRequestStream())
                {
                    stream1.Write(data, 0, data.Length);
                }
                if (int.TryParse(textBox5.Text, out int outin))
                    request.Timeout = outin;
                else
                    request.Timeout = 10000;

              var  response = request.GetResponse();
               var stream = response.GetResponseStream();
              var  strReader = new StreamReader(stream);
              string  text =  strReader.ReadToEnd();
                if (text.Replace("-----","").Length>7)
                {
                    string[] str = Regex.Split(text, "-----");
                    itag =1;
                    ret[0] = str[1];
                    ret[1] = str[2];
                    ret[3] = itag.ToString();
                    ret[2] = str[0];
                    return ret;
                }

            }
            catch
            {

            }

            ret[3] = itag.ToString();

            return ret;



        }
        protected string[] mywhois(string url)
        {
            string[] ret = { "", "", "", "" };
            int itag = 0;
            url = url.Replace(" ", "").Replace("\\", "/").Replace("http://", "").Replace("https://", "").Split('/')[0].Split('?')[0];


            try
            {


                string wurl = "162.19.186.252";
                var tcpWhois = new TcpClient(wurl, 8080);
                tcpWhois.SendTimeout= 200000;
                tcpWhois.ReceiveTimeout = 200000;

                //SETUP THE NETWORK STREAM
                var nsWhois = tcpWhois.GetStream();

                //GET THE DATA IN THE BUFFER FROM THE NETWORK STREAM
                var bfWhois = new BufferedStream(nsWhois);

                var strmSend = new StreamWriter(bfWhois);

                strmSend.WriteLine(url);

                strmSend.Flush();


                var strmRecive = new StreamReader(bfWhois);
                StringBuilder stb = new StringBuilder();
                string response1;
                while ((response1 = strmRecive.ReadLine()) != null)
                {
                    stb.Append(response1);
                    itag = 1;
                    if (response1.Contains("last-updated:"))
                        ret[0] = response1.Replace("last-updated:", "").Replace(" ", "").Replace("	", "").Trim();

                    if (response1.Contains("expire-date:"))
                        ret[1] = response1.Replace("expire-date:", "").Replace(" ", "").Replace("	", "").Trim(); ;
                    if (response1.Contains("Updated Date:"))
                        ret[0] = response1.Replace("Updated Date:", "").Replace(" ", "").Replace("	", "").Trim(); ;
                    if (response1.Contains("Registry Expiry Date:"))
                        ret[1] = response1.Replace("Registry Expiry Date:", "").Replace(" ", "").Replace("	", "").Trim(); ;

                }
                if (itag == 1)
                {
                    ret[3] = itag.ToString();
                    ret[2] = stb.ToString();
                    return ret;
                }
            }
            catch
            {

            }

            ret[3] = itag.ToString();

            return ret;



        }
        protected string[] whois(string url)
        {
            string[] ret = { "", "", "", "" };
            int itag = 0;
            url = url.Replace(" ", "").Replace("\\", "/").Replace("http://", "").Replace("https://", "").Split('/')[0].Split('?')[0];
            

            try
            {


                string wurl = getinaa(url);
                var tcpWhois = new TcpClient(wurl, 43);


                //SETUP THE NETWORK STREAM
                var nsWhois = tcpWhois.GetStream();

                //GET THE DATA IN THE BUFFER FROM THE NETWORK STREAM
                var bfWhois = new BufferedStream(nsWhois);

                var strmSend = new StreamWriter(bfWhois);

                strmSend.WriteLine(url);

                strmSend.Flush();


                var strmRecive = new StreamReader(bfWhois);
                StringBuilder stb = new StringBuilder();
                string response1;
                while ((response1 = strmRecive.ReadLine()) != null)
                {
                    stb.Append(response1);
                    itag = 1;
                    if (response1.Contains("last-updated:"))
                        ret[0] = response1.Replace("last-updated:", "").Replace(" ", "").Replace("	", "").Trim();

                    if (response1.Contains("expire-date:"))
                        ret[1] = response1.Replace("expire-date:", "").Replace(" ", "").Replace("	", "").Trim(); ;
                    if (response1.Contains("Updated Date:"))
                        ret[0] = response1.Replace("Updated Date:", "").Replace(" ", "").Replace("	", "").Trim(); ;
                    if (response1.Contains("Registry Expiry Date:"))
                        ret[1] = response1.Replace("Registry Expiry Date:", "").Replace(" ", "").Replace("	", "").Trim(); ;

                }
                if (itag == 1)
                {
                    ret[3] = itag.ToString();
                    ret[2] = stb.ToString();
                    return ret;
                }
            }
            catch
            {

            }

            ret[3] = itag.ToString();

            return ret;



        }
        private string getinaa(string tld)
        {

            string url = "";
            string[] us = tld.Split('.');
            string pat = us[us.Length - 1];

            SqlConnection cnn = new SqlConnection(ConfigurationManager.ConnectionStrings["pliconnectionstring"].ConnectionString);
            SqlCommand cmd1;
            SqlDataReader reader;

           Boolean has = false;
            cnn.Close(); cnn.Open();
            cmd1 = new SqlCommand("select server from [iana] where pat =@pat", cnn);
            cmd1.Parameters.AddWithValue("@pat", pat);
            reader = cmd1.ExecuteReader();
            while (reader.Read())
            {
                has = true;
                url = reader[0].ToString();
                break;
            }
            cnn.Close();
            if (has&&url!="")
                return url;
            try
            {

                var tcpWhois = new TcpClient("whois.iana.org", 43);
                var nsWhois = tcpWhois.GetStream();

                //GET THE DATA IN THE BUFFER FROM THE NETWORK STREAM
                var bfWhois = new BufferedStream(nsWhois);

                var strmSend = new StreamWriter(bfWhois);

                strmSend.WriteLine(tld);

                strmSend.Flush();
                try
                {
                    var strmRecive = new StreamReader(bfWhois);
                    string response;
                    StringBuilder stb = new StringBuilder();

                    while ((response = strmRecive.ReadLine()) != null)
                    {
                        if (response.StartsWith("whois:"))
                        {
                            url = response.Replace("whois:", "").Replace(" ", "");
                           
                        }
                        stb.Append(response);
                    }

                    if (!has)
                    {
                        cnn.Close(); cnn.Open();
                        cmd1 = new SqlCommand("insert into [iana] (pat,server,source) values (@pat,@server,@source) ", cnn);
                        cmd1.Parameters.AddWithValue("@pat", pat);
                        cmd1.Parameters.AddWithValue("@server", url);
                        cmd1.Parameters.AddWithValue("@source", stb.ToString());
                        cmd1.ExecuteNonQuery();
                        cnn.Close();
                    }
                    else
                    {
                        cnn.Close(); cnn.Open();
                        cmd1 = new SqlCommand("update [iana] set server=@server,source=@source where pat=@pat ", cnn);
                        cmd1.Parameters.AddWithValue("@pat", pat);
                        cmd1.Parameters.AddWithValue("@server", url);
                        cmd1.Parameters.AddWithValue("@source", stb.ToString());
                        cmd1.ExecuteNonQuery();
                        cnn.Close();
                    }
                }

                catch
                {
                }
            }
            catch
            {

                
            }

            if (url == "")
            {

                try
                {
                    ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };
                    HttpWebRequest request = (HttpWebRequest)HttpWebRequest.Create("https://www.iana.org/whois?q=" + tld);
                    request.UserAgent = useragentall;
                    request.UserAgent = useragentall;
                    var response = (HttpWebResponse)request.GetResponse();

                    Stream stream = response.GetResponseStream();
                    StreamReader strReader = new StreamReader(stream);
                    string text = strReader.ReadToEnd();
                    if (text != "")
                    {

                        foreach (string str in Regex.Split(text, "\n"))
                        {
                            if (str.StartsWith("whois:"))
                            {
                                url = str.Replace("whois:", "").Replace(" ", "");
                                break;
                            }
                        }
                        if (!has)
                        {
                            cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("insert into [iana] (pat,server,source) values (@pat,@server,@source) ", cnn);
                            cmd1.Parameters.AddWithValue("@pat", pat);
                            cmd1.Parameters.AddWithValue("@server", url);
                            cmd1.Parameters.AddWithValue("@source", text);
                            cmd1.ExecuteNonQuery();
                            cnn.Close();
                        }
                        else
                        {
                            cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("update [iana] set server=@server,source=@source where pat=@pat ", cnn);
                            cmd1.Parameters.AddWithValue("@pat", pat);
                            cmd1.Parameters.AddWithValue("@server", url);
                            cmd1.Parameters.AddWithValue("@source", text);
                            cmd1.ExecuteNonQuery();
                            cnn.Close();
                        }

                    }
                }
                catch
                {
                }

            }
            return url;
        }


        private void button4_Click(object sender, EventArgs e)
        {

            if (!start2)
            {
                tokenSource2 = new CancellationTokenSource();
                CancellationToken ct = tokenSource2.Token;
                start2 = true;
                task2 = Task.Run(() => startwork2(), tokenSource2.Token);
                button4.Enabled = false;
                button3.Enabled = true;
            }
        }

        private void button3_Click(object sender, EventArgs e)
        {

            if (start2)
            {
                tokenSource2.Cancel();
                tokenSource2.Dispose();
                start2 = false;
                label5.Text = "Stop at " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss");

                listBox2.DataSource = null;
                button3.Enabled = false;
                button4.Enabled = true;
            }
        }

        public async Task startwork2()
        {
            while (start2)
            {
                label5.Text = "Start proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task2.Status.ToString();
                await GetResponseAsync2();

                label5.Text = "Compelet proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " And go to sleep for " + textBox1.Text + " minutes " + task2.Status.ToString();
                await Task.Delay(int.Parse(textBox1.Text) * 1000 * 60);

            }
        }
        public async Task GetResponseAsync2()
        {
            listBox2.Items.Clear();

            listBox3.Items.Clear();

            if (checkBox1.Checked)
            {
                Random r1 = new Random();
                string[] useragent = { "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1", "Mozilla/5.0 (iPad; CPU OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1", "Mozilla/5.0 (iPod touch; CPU iPhone 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.2; rv:110.0) Gecko/20100101 Firefox/110.0", "Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0", "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:110.0) Gecko/20100101 Firefox/110.0", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:110.0) Gecko/20100101 Firefox/110.0", "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/110.0 Mobile/15E148 Safari/605.1.15", "Mozilla/5.0 (iPad; CPU OS 13_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/110.0 Mobile/15E148 Safari/605.1.15", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/110.0.5481.114 Mobile/15E148 Safari/604.1", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57", "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57", "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57" };
                SqlConnection cnn2 = new SqlConnection(ConfigurationManager.ConnectionStrings["pliconnectionstring"].ConnectionString);
                SqlCommand cmd2;
                SqlDataReader reader2;
                List<urlph> deturl = new List<urlph>();
                cnn2.Open();
                cmd2 = new SqlCommand("select idphish,url from phishdata where source is not null and url like N'%email-protection%'", cnn2);
                reader2 = cmd2.ExecuteReader();
                while (reader2.Read())
                {
                    deturl.Add(new urlph { id = reader2["idphish"].ToString(), url = reader2["url"].ToString() });
                }
                cnn2.Close();
                Boolean has = false;
                string besturl = "";
                string mainurl = "";
                string mainid = "";
                int row = 0;
                foreach (urlph li1 in deturl)
                {
                    row++;
                    try
                    {
                        has = false;
                        label5.Text = "Start proccess " + li1.id + " on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task2.Status.ToString();
                        if (!start2)
                        {
                            return;
                        }
                        mainurl = "";
                        mainid = "";
                        besturl = "";
                        string use= useragent[r1.Next(0, useragent.Length)];
                        //HttpWebRequest request = (HttpWebRequest)WebRequest.Create("https://phishtank.org/phish_detail.php?phish_id=" + li1.id);
                        //request.Method = "GET";
                        //request.UserAgent = use;
                        //request.Timeout = int.Parse(textBox5.Text);
                        //request.AllowAutoRedirect = false;
                        //HttpWebResponse response = (HttpWebResponse)request.GetResponse();

                        HttpWebRequest request1 = (HttpWebRequest)WebRequest.Create("https://phishtank.org/view_phish_redirect.php?phish_id=" + li1.id);
                        request1.Method = "GET";
                        request1.CookieContainer = new CookieContainer();
                        System.Net.Cookie co = new System.Net.Cookie();
                        co.Name = "PHPSESSID";
                        co.Value = "kulekcclb1cnr59kl7trd7se8a8r66ja";
                       // request1.CookieContainer.Add(co);
                        

                        request1.Timeout = int.Parse(textBox5.Text);

                        request1.UserAgent = use;
                        request1.AllowAutoRedirect = false;
                        HttpWebResponse response1 = (HttpWebResponse)request1.GetResponse();
                        foreach (string str in Regex.Split(response1.Headers.ToString(), "\n"))
                        {
                            if (str.StartsWith("Location:"))
                            {
                                besturl = Regex.Split(str, "Location:")[1];
                                if (besturl.Contains(Regex.Split(li1.url, "<a")[0]))
                                {
                                    mainurl = besturl;
                                    mainid = li1.id;
                                    has = true;
                                    break;
                                }
                            }
                            else if(str.ToLower().StartsWith("location:"))
                            {
                                besturl = Regex.Split(str.ToLower(), "location:")[1];
                                if (besturl.Contains(Regex.Split(li1.url.ToLower(), "<a")[0]))
                                {
                                    mainurl = besturl;
                                    mainid = li1.id;
                                    has = true;
                                    break;
                                }
                            }

                        }
                        if (!has)
                        {
                            listBox3.Items.Add(li1.id + " --> " + li1.url);
                            continue;
                        }

                        string[] conect = { ConfigurationManager.ConnectionStrings["pliconnectionstring"].ConnectionString
                                  , "Data Source=.;Initial Catalog=tarair_phdata0904;Persist Security Info=True;User=mojtabasqldatabase; password=#P@rspaS##S"
                                    , "Data Source=.;Initial Catalog=tarair_phdata0910;Persist Security Info=True;User=mojtabasqldatabase; password=#P@rspaS##S"
                                   , "Data Source=.;Initial Catalog=tarair_phdata1015;Persist Security Info=True;User=mojtabasqldatabase; password=#P@rspaS##S"
                                   };
                        foreach (string constr in conect)
                        {
                            try
                            {

                                SqlConnection cnn = new SqlConnection(constr);
                                SqlCommand cmd1;
                                SqlDataReader reader;
                                Boolean avail = false;
                                cnn.Close(); cnn.Open();
                                cmd1 = new SqlCommand("select id from phishdata where idphish=@id", cnn);
                                cmd1.Parameters.AddWithValue("@id", mainid);
                                reader = cmd1.ExecuteReader();
                                while (reader.Read())
                                {
                                    avail = true;
                                }
                                cnn.Close();
                                if (avail)
                                {
                                    if (mainurl != "")
                                    {

                                        cnn.Close(); cnn.Open();
                                        cmd1 = new SqlCommand("update phishdata set url=@url where idphish=@id", cnn);
                                        cmd1.Parameters.AddWithValue("@id", mainid);
                                        cmd1.Parameters.AddWithValue("@url", mainurl);
                                        cmd1.ExecuteNonQuery();
                                        cnn.Close();
                                    }
                                }
                            }
                            catch (Exception ex)
                            {
                                MessageBox.Show(ex.ToString());
                            }
                        }

                    }
                    catch (Exception ex)
                    {
                        listBox3.Items.Add(li1.id);
                    }
                    label5.Text = "Delay proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " And go to sleep for 10 secound " + task2.Status.ToString();

                    await Task.Delay( 10000 );
                    
                    mainurl = "";
                    mainid = "";
                }
                return;
            }
            else
            {

                try
                {

                    SqlConnection cnn = new SqlConnection(ConfigurationManager.ConnectionStrings["pliconnectionstring"].ConnectionString);
                    SqlCommand cmd1;
                    SqlDataReader reader;
                    List<string> allurl = new List<string>();
                    int ecount = 100;
                    if (int.TryParse(textBox6.Text, out int outsete))
                        ecount = outsete;
                    cnn.Close(); cnn.Open();
                    cmd1 = new SqlCommand("select url from phishdata where source is null and countsource<=@outsete order by id desc", cnn);
                    cmd1.Parameters.AddWithValue("@outsete", outsete);
                    reader = cmd1.ExecuteReader();
                    while (reader.Read())
                    {
                        allurl.Add(reader["url"].ToString());
                    }
                    cnn.Close();
                    string noprocess = "";

                    ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };
                    HttpWebRequest request;
                    Stream stream;
                    WebResponse response;
                    StreamReader strReader;
                    string text;

                    listBox2.Items.Clear();
                    try
                    {
                        listBox2.DataSource = allurl;
                    }
                    catch
                    {

                    }
                    while (allurl.Count > 0 && start2)
                    {
                        noprocess = allurl[0];
                        label5.Text = "Start proccess " + noprocess + " on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task2.Status.ToString();
                        try
                        {
                            request = (HttpWebRequest)HttpWebRequest.Create(noprocess);
                            request.UserAgent = useragentall;
                            if (int.TryParse(textBox5.Text, out int outi))
                                request.Timeout = outi;
                            else
                                request.Timeout = 10000;

                            response = request.GetResponse();
                            stream = response.GetResponseStream();
                            strReader = new StreamReader(stream);
                            text = await strReader.ReadToEndAsync();

                            cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("update phishdata set source=@source,countsource=countsource+1 where url=@url", cnn);
                            cmd1.Parameters.AddWithValue("@url", noprocess);
                            cmd1.Parameters.AddWithValue("@source", text);
                            cmd1.ExecuteNonQuery();
                            cnn.Close();
                            allurl.Remove(noprocess);
                        }
                        catch
                        {

                            allurl.Remove(noprocess);

                            cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("update phishdata set countsource=countsource+1 where url=@url", cnn);
                            cmd1.Parameters.AddWithValue("@url", noprocess);
                            cmd1.ExecuteNonQuery();
                            cnn.Close();
                            listBox3.Items.Add("error in " + noprocess);

                        }
                    }

                    listBox2.DataSource = null;
                }
                catch (Exception ex)
                {

                    listBox2.DataSource = null;
                    listBox3.Items.Add("error in " + ex);

                }
            }
        }
        private void ListBox1_KeyDown(object sender, System.Windows.Forms.KeyEventArgs e)
        {
            ListBox l1 = (ListBox)sender;
            if (e.Control && e.KeyCode == System.Windows.Forms.Keys.C)
            {
                System.Text.StringBuilder copy_buffer = new System.Text.StringBuilder();
                foreach (object item in l1.SelectedItems)
                    copy_buffer.AppendLine(item.ToString());
                if (copy_buffer.Length > 0)
                    Clipboard.SetText(copy_buffer.ToString());
            }
        }

        private void button6_Click(object sender, EventArgs e)
        {
            if (!start3)
            {
                tokenSource3 = new CancellationTokenSource();
                CancellationToken ct = tokenSource3.Token;
                start3 = true;
                task3 = Task.Run(() => startwork3(), tokenSource3.Token);
                button6.Enabled = false;
                button5.Enabled = true;
            }
        }

        private void button5_Click(object sender, EventArgs e)
        {
            if (start3)
            {
                tokenSource3.Cancel();
                tokenSource3.Dispose();
                start3 = false;
                label11.Text = "Stop at " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss");

                listBox4.DataSource = null;
                button5.Enabled = false;
                button6.Enabled = true;
            }
        }

        public async Task startwork3()
        {
            while (start3)
            {
                label11.Text = "Start proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task3.Status.ToString();
                GetResponseAsync3();

                label11.Text = "Compelet proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " And go to sleep for " + textBox7.Text + " minutes " + task3.Status.ToString();
                await Task.Delay(int.Parse(textBox7.Text) * 1000 * 60);

            }
        }
        public void GetResponseAsync3()
        {
            listBox4.Items.Clear();

            listBox5.Items.Clear();
            try
            {

                SqlConnection cnn = new SqlConnection(ConfigurationManager.ConnectionStrings["pliconnectionstring"].ConnectionString);
                SqlCommand cmd1;
                SqlDataReader reader;
                string noprocess = "";
                List<string> allurl = new List<string>();
                int ecount = 100;
                if (int.TryParse(textBox2.Text, out int outsete))
                    ecount = outsete;

                cnn.Close(); cnn.Open();
                cmd1 = new SqlCommand("select url from phishdata where dnsall is null and countdns<=@outsete order by id desc", cnn);
                cmd1.Parameters.AddWithValue("@outsete", outsete);
                reader = cmd1.ExecuteReader();
                while (reader.Read())
                {
                    allurl.Add(reader["url"].ToString());
                }
                cnn.Close();

                listBox4.Items.Clear();
                try
                {
                    listBox4.DataSource = allurl;
                }
                catch
                {

                }
                while (allurl.Count > 0&&start3)
                {
                    noprocess = allurl[0];
                    label11.Text = "Start proccess " + noprocess + " on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task3.Status.ToString();
                    try
                    {
                        string[] str;
                        if (whoamirun=="Iran")
                             str = iranwhois(noprocess);
                        else
                            str = whois(noprocess);
                        //  string[] str = mywhois("google.com");
                        //  return;

                        if (str[3] == "1")
                        {
                            cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("update phishdata set dnsall=@dnsall,dnsr1=@dnsr1,dnsr2=@dnsr2,countdns=countdns+1 where url=@url", cnn);
                            cmd1.Parameters.AddWithValue("@url", noprocess);
                            cmd1.Parameters.AddWithValue("@dnsall", str[2]);
                            cmd1.Parameters.AddWithValue("@dnsr1", str[0]);
                            cmd1.Parameters.AddWithValue("@dnsr2", str[1]);
                            cmd1.ExecuteNonQuery();
                            cnn.Close();
                        }
                        else
                        {
                            cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("update phishdata set countdns=countdns+1 where url=@url", cnn);
                            cmd1.Parameters.AddWithValue("@url", noprocess);
                            cmd1.ExecuteNonQuery();
                            cnn.Close();
                            listBox5.Items.Add("error in " + noprocess);
                        }
                        allurl.Remove(noprocess);
                    }
                    catch (Exception ex)
                    {

                        allurl.Remove(noprocess);

                        cnn.Close(); cnn.Open();
                        cmd1 = new SqlCommand("update phishdata set countdns=countdns+1 where url=@url", cnn);
                        cmd1.Parameters.AddWithValue("@url", noprocess);
                        cmd1.ExecuteNonQuery();
                        cnn.Close();
                        listBox5.Items.Add("error in " + noprocess + ex);

                    }
                }

                listBox4.DataSource = null;
            }
            catch (Exception ex)
            {

                listBox4.DataSource = null;
                listBox5.Items.Add("error in " + ex);

            }
        }

        private void button8_Click(object sender, EventArgs e)
        {
            if (!start4)
            {
                tokenSource4 = new CancellationTokenSource();
                CancellationToken ct = tokenSource4.Token;
                start4 = true;
                task4 = Task.Run(() => startwork4(), tokenSource4.Token);
                button8.Enabled = false;
                button7.Enabled = true;
            }
        }

        private void button7_Click(object sender, EventArgs e)
        {
            if (start4)
            {
                tokenSource4.Cancel();
                tokenSource4.Dispose();
                start4 = false;
                label16.Text = "Stop at " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss");

                listBox6.DataSource = null;
                button7.Enabled = false;
                button8.Enabled = true;
            }
        }

        public async Task startwork4()
        {
            while (start4)
            {
                label16.Text = "Start proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task4.Status.ToString();
                GetResponseAsync4();

                label16.Text = "Compelet proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " And go to sleep for " + textBox8.Text + " minutes " + task4.Status.ToString();
                await Task.Delay(int.Parse(textBox8.Text) * 1000 * 60);

            }
        }
        public void GetResponseAsync4()
        {
            listBox6.Items.Clear();

            listBox7.Items.Clear();
            try
            {

                SqlConnection cnn = new SqlConnection(ConfigurationManager.ConnectionStrings["pliconnectionstring"].ConnectionString);
                SqlCommand cmd1;
                SqlDataReader reader;
                string noprocess = "";
                List<string> allurl = new List<string>();
                int ecount = 100;
                if (int.TryParse(textBox4.Text, out int outsete))
                    ecount = outsete;

                cnn.Close(); cnn.Open();
                cmd1 = new SqlCommand("select url from phishdata where hasssl is null and countssl<=@outsete order by id desc", cnn);
                cmd1.Parameters.AddWithValue("@outsete", outsete);
                reader = cmd1.ExecuteReader();
                while (reader.Read())
                {
                    allurl.Add(reader["url"].ToString());
                }
                cnn.Close();

                listBox6.Items.Clear();
                try
                {
                    listBox6.DataSource = allurl;
                }
                catch
                {

                }
                while (allurl.Count > 0&&start4)
                {
                    noprocess = allurl[0];
                    label16.Text = "Start proccess " + noprocess + " on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task4.Status.ToString();
                    try
                    {
                        string[] str = onlinessl(noprocess);
                        if (str[0] != "")
                        {
                            cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("update phishdata set hasssl=@hasssl,ssl1=@ssl1,ssl2=@ssl2,ssl3=@ssl3,countssl=countssl+1 where url=@url", cnn);
                            cmd1.Parameters.AddWithValue("@url", noprocess);
                            cmd1.Parameters.AddWithValue("@hasssl", str[0]);
                            cmd1.Parameters.AddWithValue("@ssl1", str[1]);
                            cmd1.Parameters.AddWithValue("@ssl2", str[2]);
                            cmd1.Parameters.AddWithValue("@ssl3", str[3]);
                            cmd1.ExecuteNonQuery();
                            cnn.Close();
                        }
                        else
                        {
                            cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("update phishdata set countssl=countssl+1 where url=@url", cnn);
                            cmd1.Parameters.AddWithValue("@url", noprocess);
                            cmd1.ExecuteNonQuery();
                            cnn.Close();
                            listBox7.Items.Add("error in " + noprocess);
                        }
                        allurl.Remove(noprocess);
                    }
                    catch (Exception ex)
                    {

                        allurl.Remove(noprocess);

                        cnn.Close(); cnn.Open();
                        cmd1 = new SqlCommand("update phishdata set countssl=countssl+1 where url=@url", cnn);
                        cmd1.Parameters.AddWithValue("@url", noprocess);
                        cmd1.ExecuteNonQuery();
                        cnn.Close();
                        listBox7.Items.Add("error in " + noprocess + ex);

                    }
                }

                listBox6.DataSource = null;
            }
            catch (Exception ex)
            {

                listBox6.DataSource = null;
                listBox7.Items.Add("error in " + ex);

            }
        }
        public void sendmail(string idphish)
        {
            try
            {
                SmtpClient smtpClient = new SmtpClient("mail.hormozgan.ac.ir", 587);

                smtpClient.Credentials = new System.Net.NetworkCredential("shokoh@hormozgan.ac.ir", "mojtaba50!");
                // smtpClient.UseDefaultCredentials = true; // uncomment if you don't want to use the network credentials
                smtpClient.DeliveryMethod = SmtpDeliveryMethod.Network;
                smtpClient.EnableSsl = true;
                MailMessage mail = new MailMessage();

                //Setting From , To and CC
                mail.From = new MailAddress("shokoh@hormozgan.ac.ir");
                mail.To.Add(new MailAddress("shokoh@hormozgan.ac.ir"));
                mail.Subject = "phish id " + idphish;
                mail.Body = "<a href=\"https://phishtank.org/phish_detail.php?phish_id=" + idphish + "\" >https://phishtank.org/phish_detail.php?phish_id=" + idphish + " </a><h1>"+whoamirun+"</h1>";
                smtpClient.SendAsync(mail, null);
            }
            catch
            { }
        }

        private void button9_Click(object sender, EventArgs e)
        {
            string[] conect = { ConfigurationManager.ConnectionStrings["pliconnectionstring"].ConnectionString
            , "Data Source=.;Initial Catalog=tarair_phdata0904;Persist Security Info=True;User=mojtabasqldatabase; password=#P@rspaS##S"
             , "Data Source=.;Initial Catalog=tarair_phdata0910;Persist Security Info=True;User=mojtabasqldatabase; password=#P@rspaS##S"
             , "Data Source=.;Initial Catalog=tarair_phdata1015;Persist Security Info=True;User=mojtabasqldatabase; password=#P@rspaS##S"
            };
            foreach (string constr in conect)
            {
                try
                {

                    SqlConnection cnn = new SqlConnection(constr);
                    SqlCommand cmd1;
                    SqlDataReader reader;
                    Boolean avail = false;
                    cnn.Close(); cnn.Open();
                    cmd1 = new SqlCommand("select id from phishdata where idphish=@id", cnn);
                    cmd1.Parameters.AddWithValue("@id", textBox10.Text.Trim());
                    reader = cmd1.ExecuteReader();
                    while (reader.Read())
                    {
                        avail = true;
                    }
                    cnn.Close();
                    if (avail)
                    {
                        if (textBox9.Text != "")
                        {

                            cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("update phishdata set url=@url where idphish=@id", cnn);
                            cmd1.Parameters.AddWithValue("@id", textBox10.Text.Trim());
                            cmd1.Parameters.AddWithValue("@url", textBox9.Text.Replace("&amp;", "&").Trim());
                            cmd1.ExecuteNonQuery();
                            cnn.Close();
                        }
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.ToString());
                }
            }


            textBox9.Text = "";
            textBox10.Text = "";
        }

        private void button11_Click(object sender, EventArgs e)
        {
            if (!start5)
            {
                tokenSource5 = new CancellationTokenSource();
                CancellationToken ct = tokenSource5.Token;
                start5 = true;
                task5 = Task.Run(() => startwork5(), tokenSource5.Token);
                button11.Enabled = false;
                button10.Enabled = true;
            }
        }

        private void button10_Click(object sender, EventArgs e)
        {

            if (start5)
            {
                tokenSource5.Cancel();
                tokenSource5.Dispose();
                start5 = false;
                label23.Text = "Stop at " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss");

                listBox8.DataSource = null;
                button10.Enabled = false;
                button11.Enabled = true;
                try
                {
                        driver.Quit();
                }
                catch
                {

                }
            }
        }


        public async Task startwork5()
        {
            while (start5)
            {
                label23.Text = "Start proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task5.Status.ToString();
                GetResponseAsync5();

                label23.Text = "Compelet proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " And go to sleep for " + textBox12.Text + " minutes " + task5.Status.ToString();
                await Task.Delay(int.Parse(textBox12.Text) * 1000 * 60);

            }
        }
        public class urlidn
            {
           public string str { get; set; }
            public string id { get; set; }
        }
        public void GetResponseAsync5()
        {
            listBox8.Items.Clear();

            listBox9.Items.Clear();
            try
            {
                string subPath = Environment.CurrentDirectory+"/ImagesPath"; // Your code goes here

                bool exists = System.IO.Directory.Exists(subPath);

                if (!exists)
                    System.IO.Directory.CreateDirectory(subPath);
                SqlConnection cnn = new SqlConnection(ConfigurationManager.ConnectionStrings["pliconnectionstring"].ConnectionString);
                SqlCommand cmd1;
                SqlDataReader reader;
                string noprocess = "";
                List<string> allurl = new List<string>();
                List<urlidn> allurlid = new List<urlidn>();
                int ecount = 100;
                if (int.TryParse(textBox11.Text, out int outsete))
                    ecount = outsete;
                var options = new ChromeOptions();
                options.AddArguments(new List<string>() { "--headless", "--no-sandbox", "--disable-gpu", "--ignore-certificate-errors", "--disable-extensions", "--disable-dev-shm-usage" });
                try
                {
                    if (driver == null || driver.Url == "")
                        driver = new ChromeDriver(Environment.CurrentDirectory, options, TimeSpan.FromMinutes(1));
                }
                catch
                {

                    driver = new ChromeDriver(Environment.CurrentDirectory, options, TimeSpan.FromMinutes(1));
                }

                cnn.Close(); cnn.Open();
                cmd1 = new SqlCommand("select url,idphish from phishdata where  screen is null and source is not null and countscreen<=@outsete order by id desc", cnn);
                cmd1.Parameters.AddWithValue("@outsete", outsete);
                reader = cmd1.ExecuteReader();
                while (reader.Read())
                {
                    allurl.Add(reader["url"].ToString());
                    allurlid.Add(new urlidn{  str= reader["url"].ToString(),id= reader["idphish"].ToString() });
                }
                cnn.Close();

                listBox8.Items.Clear();
                try
                {
                    listBox8.DataSource = allurl;
                }
                catch
                {

                }
                while (allurl.Count > 0&&start5)
                {
                    noprocess = allurl[0];
                    label23.Text = "Start proccess " + noprocess + " on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task5.Status.ToString();
                    try
                    {
                        string idofurl = "noid";
                        try
                        {
                            idofurl = allurlid.First(x => x.str == noprocess).id;
                        }
                        catch
                        {

                            cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("select idphish from phishdata where url=@url", cnn);
                            cmd1.Parameters.AddWithValue("@url", noprocess);
                            reader = cmd1.ExecuteReader();
                            while (reader.Read())
                            {
                                idofurl = reader["idphish"].ToString();
                            }
                            cnn.Close();
                        }
                        int timeout = 10000;
                        if (int.TryParse(textBox5.Text, out int outi))
                            timeout = outi;
                        else
                            timeout = 10000;

                        /*
                        var screenshotJob = ScreenshotJobBuilder.Create(noprocess)
                         .SetBrowserSize(1920, 768)
                        .SetCaptureZone(CaptureZone.FullPage)
                         .SetTrigger(new WindowLoadTrigger())
                         .SetTimeout(timeout)
                         .SetUserAgent(useragentall)
                         ;

                        System.Drawing.Image screenshot = screenshotJob.Freeze();
                        screenshot.Save(subPath +"/"+ idofurl+"_1.jpg");
                        var screenshotJob1 = ScreenshotJobBuilder.Create(noprocess)
                         .SetBrowserSize(360, 740)
                        .SetCaptureZone(CaptureZone.FullPage)
                         .SetTrigger(new WindowLoadTrigger())
                         .SetTimeout(timeout)
                         .SetUserAgent(useragentall)
                         ;

                        System.Drawing.Image screenshot1 = screenshotJob1.Freeze();
                        screenshot1.Save(subPath + "/" + idofurl + "_2.jpg");
                        var chromeOptions = new ChromeOptions
                        {
                            BinaryLocation = @"C:\Users\2-as Aukstas\AppData\Local\Google\Chrome SxS\Application\chrome.exe",
                            //DebuggerAddress = "127.0.0.1:9222"
                        };

                        chromeOptions.AddArguments(new List<string>() { "no-sandbox", "headless", "disable-gpu" });
                       */
                        //  var options = new ChromeOptions();

                        if (driver == null)
                            driver = new ChromeDriver(Environment.CurrentDirectory, options, TimeSpan.FromMinutes(1));
                        options.AddArguments(new List<string>() { "--headless", "--no-sandbox", "--disable-gpu", "--ignore-certificate-errors", "--disable-extensions", "--disable-dev-shm-usage" });

                       // driver = new ChromeDriver(options);
                        driver.Navigate().GoToUrl(noprocess);
                        var size = new Size(360, 740);
                        driver.Manage().Window.Size = size;
                        OpenQA.Selenium.Screenshot TakeScreenshot = ((ITakesScreenshot)driver).GetScreenshot();
                        
                        TakeScreenshot.SaveAsFile(subPath + "/" + idofurl + "_2.jpg");
                       // driver = new ChromeDriver(options);
                        driver.Navigate().GoToUrl(noprocess);
                        size = new Size(1920, 768);
                        driver.Manage().Window.Size = size;
                        OpenQA.Selenium.Screenshot TakeScreenshot1 = ((ITakesScreenshot)driver).GetScreenshot();

                        TakeScreenshot1.SaveAsFile(subPath + "/" + idofurl + "_1.jpg");




                        cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("update phishdata set screen=1,countscreen=countscreen+1 where url=@url", cnn);
                            cmd1.Parameters.AddWithValue("@url", noprocess);
                            cmd1.ExecuteNonQuery();
                            cnn.Close();
                        allurl.Remove(noprocess);
                    }
                    catch (Exception ex)
                    {
                        allurl.Remove(noprocess);

                        cnn.Close(); cnn.Open();
                        cmd1 = new SqlCommand("update phishdata set countscreen=countscreen+1 where url=@url", cnn);
                        cmd1.Parameters.AddWithValue("@url", noprocess);
                        cmd1.ExecuteNonQuery();
                        cnn.Close();
                        listBox9.Items.Add("error in " + noprocess + ex);

                    }
                }

                listBox8.DataSource = null;
            }
            catch (Exception ex)
            {

                listBox8.DataSource = null;
                listBox9.Items.Add("error in " + ex);

            }
        }

        private void button13_Click(object sender, EventArgs e)
        {

            if (!start6)
            {
                tokenSource6 = new CancellationTokenSource();
                CancellationToken ct = tokenSource6.Token;
                start6 = true;
                task6 = Task.Run(() => startwork6(), tokenSource6.Token);
                button13.Enabled = false;
                button12.Enabled = true;
            }
        }

        private void button12_Click(object sender, EventArgs e)
        {

            if (start6)
            {
                tokenSource6.Cancel();
                tokenSource6.Dispose();
                start6 = false;
                label27.Text = "Stop at " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss");

                listBox10.DataSource = null;
                button12.Enabled = false;
                button13.Enabled = true;
            }
        }


        public async Task startwork6()
        {
            while (start6)
            {
                label27.Text = "Start proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task6.Status.ToString();
                  await  GetResponseAsync6();

                label27.Text = "Compelet proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " And go to sleep for " + textBox14.Text + " minutes " + task6.Status.ToString();
                await Task.Delay(int.Parse(textBox14.Text) * 1000 * 60);

            }
        }
        public void getcrawl()
        {
            try
            {
                SqlConnection cnn = new SqlConnection(ConfigurationManager.ConnectionStrings["pliconnectionstring"].ConnectionString);
                SqlCommand cmd1;
                SqlDataReader reader;
                string noprocess = "";
                List<urlph> allurlid = new List<urlph>();
                int ecount = 100;
                if (int.TryParse(textBox13.Text, out int outsete))
                    ecount = outsete;

                cnn.Close(); cnn.Open();
                cmd1 = new SqlCommand("select url,idphish,source from phishdata where source is not null and crawl is null and countCrawl<=@outsete order by id desc", cnn);
                cmd1.Parameters.AddWithValue("@outsete", outsete);
                reader = cmd1.ExecuteReader();
                while (reader.Read())
                {
                    allurlid.Add(new urlph { url = reader["url"].ToString(), id = reader["idphish"].ToString(), detail = reader["source"].ToString() });
                }
                cnn.Close();

                while (allurlid.Count > 0 && start6)
                {
                    if (!start6)
                        break;
                    noprocess = allurlid[0].url;
                    label27.Text = "Start Crawl proccess " + noprocess + " on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task6.Status.ToString();
                    try
                    {
                        string idofurl = allurlid[0].id;
                        string source = allurlid[0].detail.Replace(" ","");

                        List<string> liph = new List<string>();
                        int start = 0;
                        int end = 0;
                        string temp = "";
                        while (true)
                        {
                            start = source.IndexOf("href=\"", end);
                            if (start == -1)
                                break;
                            end = source.IndexOf("\"", start+6);
                            if (end == -1)
                                break;
                            if (end < start)
                                break;
                            try
                            {
                                temp = source.Substring(start, end - start).Replace("href=\"","");
                                if (temp.StartsWith("#"))
                                    continue;
                                if (temp == "")
                                    continue;
                                if(temp.StartsWith("http://")|| temp.StartsWith("https://"))
                                {
                                    if (!temp.Replace("http://", "https://").StartsWith("https://" + noprocess.Replace("http://", "").Replace("https://","").Split('/')[0].Split('?')[0]))
                                        continue;

                                    liph.Add(temp);
                                    continue;
                                }
                                else
                                {
                                    if (temp.StartsWith("/"))
                                    {
                                        if (noprocess.StartsWith("http://"))
                                            temp = "http://" + noprocess.Replace("http://", "").Split('/')[0].Split('?')[0] + temp.Replace("//", "/");
                                        else
                                            temp = "https://" + noprocess.Replace("https://", "").Split('/')[0].Split('?')[0] + temp.Replace("//", "/");
                                    }
                                    else
                                    {
                                        if (noprocess.EndsWith("/"))
                                            temp = noprocess + temp;
                                        else
                                            temp = noprocess + "/" + temp;
                                    }
                                }

                                liph.Add(temp);

                            }
                            catch (Exception ex)
                            { 
                            }
                        }
                         start = 0;
                         end = 0;
                        while (true)
                        {
                            start = source.IndexOf(".href='", end);
                            if (start == -1)
                                break;
                            end = source.IndexOf("'", start+8);
                            if (end == -1)
                                break;
                            if (end < start)
                                break;
                            try
                            {
                                temp = source.Substring(start, end - start).Replace(".href='","");
                                if (temp.StartsWith("#"))
                                    continue;
                                if (temp == "")
                                    continue;
                                if (temp.StartsWith("http://") || temp.StartsWith("https://"))
                                {
                                    if (!temp.Replace("http://", "https://").StartsWith("https://" + noprocess.Replace("http://", "").Replace("https://", "").Split('/')[0].Split('?')[0]))
                                        continue;
                                    liph.Add(temp);
                                    continue;
                                }
                                else
                                {
                                    if (temp.StartsWith("/"))
                                    {
                                        if (noprocess.StartsWith("http://"))
                                            temp = "http://" + noprocess.Replace("http://", "").Split('/')[0].Split('?')[0] + temp.Replace("//", "/");
                                        else
                                            temp = "https://" + noprocess.Replace("https://", "").Split('/')[0].Split('?')[0] + temp.Replace("//", "/");
                                    }
                                    else
                                    {
                                        if (noprocess.EndsWith("/"))
                                            temp = noprocess + temp;
                                        else
                                            temp = noprocess + "/" + temp;
                                    }
                                }

                                liph.Add(temp);

                            }
                            catch (Exception ex)
                            { 
                            }
                        }
                        start = 0;
                        end = 0;
                        while (true)
                        {
                            start = source.IndexOf("action=\"", end);
                            if (start == -1)
                                break;
                            end = source.IndexOf("\"", start+8);
                            if (end == -1)
                                break;
                            if (end < start)
                                break;
                            try
                            {
                                temp = source.Substring(start, end - start).Replace("action=\"", "");
                                if (temp.StartsWith("#"))
                                    continue; 
                                if (temp == "")
                                    continue;
                                if (temp.StartsWith("http://") || temp.StartsWith("https://"))
                                {
                                    if (!temp.Replace("http://", "https://").StartsWith("https://" + noprocess.Replace("http://", "").Replace("https://", "").Split('/')[0].Split('?')[0]))
                                        continue;
                                    liph.Add(temp);
                                    continue;
                                }
                                else
                                {
                                    if (temp.StartsWith("/"))
                                    {
                                        if(noprocess.StartsWith("http://"))
                                            temp = "http://" + noprocess.Replace("http://", "").Split('/')[0].Split('?')[0] + temp.Replace("//","/");
                                        else
                                            temp = "https://" + noprocess.Replace("https://", "").Split('/')[0].Split('?')[0] + temp.Replace("//", "/");
                                    }
                                    else
                                    {
                                        if (noprocess.EndsWith("/"))
                                            temp = noprocess + temp;
                                        else
                                            temp = noprocess + "/" + temp;
                                    }
                                }
                                liph.Add(temp);

                            }
                            catch (Exception ex)
                            {
                            }
                        }
                        Boolean has = false;
                        foreach (var suli in liph)
                        {
                            if (suli.EndsWith(".js") || suli.EndsWith(".css"))
                                continue;
                            has = false;
                            cnn.Close();
                            cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("select id from crawldata where url =@url and sid=@sid", cnn);
                            cmd1.Parameters.AddWithValue("@url", suli);
                            cmd1.Parameters.AddWithValue("@sid", idofurl);
                            reader = cmd1.ExecuteReader();
                            while (reader.Read())
                            {
                                has = true;
                                break;
                            }
                            cnn.Close();
                            if (!has)
                            {
                                cnn.Close();
                                cnn.Close(); cnn.Open();
                                cmd1 = new SqlCommand("insert into crawldata([sid],[url] ) values (@sid,@url)", cnn);
                                cmd1.Parameters.AddWithValue("@url", suli);
                                cmd1.Parameters.AddWithValue("@sid", idofurl);
                                cmd1.ExecuteNonQuery();
                                cnn.Close();

                            }

                        }

                        cnn.Close();
                        cnn.Close(); cnn.Open();
                        cmd1 = new SqlCommand("update phishdata set crawl=1, countscreen=countscreen+1 where url=@url", cnn);
                        cmd1.Parameters.AddWithValue("@url", noprocess);
                        cmd1.ExecuteNonQuery();
                        cnn.Close();


                        allurlid.RemoveAt(0);
                    }
                    catch (Exception ex)
                    {

                        cnn.Close();
                        allurlid.RemoveAt(0);

                        cnn.Close(); cnn.Open();
                        cmd1 = new SqlCommand("update phishdata set countscreen=countscreen+1 where url=@url", cnn);
                        cmd1.Parameters.AddWithValue("@url", noprocess);
                        cmd1.ExecuteNonQuery();
                        cnn.Close();

                    }
                }

            }
            catch (Exception ex)
            {
                listBox11.Items.Add(ex);

            }
        }

        public async Task GetResponseAsync6()
        {
            listBox10.Items.Clear();

            listBox11.Items.Clear();
            try
            {
                getcrawl();
                SqlConnection cnn = new SqlConnection(ConfigurationManager.ConnectionStrings["pliconnectionstring"].ConnectionString);
                SqlCommand cmd1;
                SqlDataReader reader;
                List<string> allurl = new List<string>();
                int ecount = 100;
                if (int.TryParse(textBox13.Text, out int outsete))
                    ecount = outsete;
                cnn.Close(); cnn.Open();
                cmd1 = new SqlCommand("select url from crawldata where source is null and countsource<=@outsete order by id desc", cnn);
                cmd1.Parameters.AddWithValue("@outsete", outsete);
                reader = cmd1.ExecuteReader();
                while (reader.Read())
                {
                    allurl.Add(reader["url"].ToString());
                }
                cnn.Close();
                string noprocess = "";

                ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };
                HttpWebRequest request;
                Stream stream;
                WebResponse response;
                StreamReader strReader;
                string text;

                listBox10.Items.Clear();
                try
                {
                    listBox10.DataSource = allurl;
                }
                catch
                {

                }
                while (allurl.Count > 0&&start6)
                {
                    noprocess = allurl[0];
                    label27.Text = "Start proccess " + noprocess + " on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task6.Status.ToString();
                    try
                    {
                        request = (HttpWebRequest)HttpWebRequest.Create(noprocess);
                        request.UserAgent = useragentall;
                        if (int.TryParse(textBox5.Text, out int outi))
                            request.Timeout = outi;
                        else
                            request.Timeout = 10000;

                        response = request.GetResponse();
                        stream = response.GetResponseStream();
                        strReader = new StreamReader(stream);
                        text = await strReader.ReadToEndAsync();

                        cnn.Close(); cnn.Open();
                        cmd1 = new SqlCommand("update crawldata set source=@source,countsource=countsource+1 where url=@url", cnn);
                        cmd1.Parameters.AddWithValue("@url", noprocess);
                        cmd1.Parameters.AddWithValue("@source", text);
                        cmd1.ExecuteNonQuery();
                        cnn.Close();
                        allurl.Remove(noprocess);
                    }
                    catch
                    {

                        allurl.Remove(noprocess);

                        cnn.Close();
                        cnn.Close(); cnn.Open();
                        cmd1 = new SqlCommand("update crawldata set countsource=countsource+1 where url=@url", cnn);
                        cmd1.Parameters.AddWithValue("@url", noprocess);
                        cmd1.ExecuteNonQuery();
                        cnn.Close();
                        listBox11.Items.Add("error in " + noprocess);

                    }
                }

                listBox10.DataSource = null;
            }
            catch (Exception ex)
            {

                listBox10.DataSource = null;
                listBox11.Items.Add("error in " + ex);

            }
        }

        private void button15_Click(object sender, EventArgs e)
        {

            if (!start7)
            {
                tokenSource7 = new CancellationTokenSource();
                CancellationToken ct = tokenSource7.Token;
                start7 = true;
                task7 = Task.Run(() => startwork7(), tokenSource7.Token);
                button15.Enabled = false;
                button14.Enabled = true;
            }
        }

        private void button14_Click(object sender, EventArgs e)
        {

            if (start7)
            {
                tokenSource7.Cancel();
                tokenSource7.Dispose();
                start7 = false;
                label31.Text = "Stop at " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss");

                listBox12.DataSource = null;
                button14.Enabled = false;
                button15.Enabled = true;
            }
        }

        public async Task startwork7()
        {
            while (start7)
            {
                label31.Text = "Start proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task7.Status.ToString();
                await GetResponseAsync7();

                label31.Text = "Compelet proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " And go to sleep for " + textBox16.Text + " minutes " + task7.Status.ToString();
                await Task.Delay(int.Parse(textBox16.Text) * 1000 * 60);

            }
        }
        public async Task GetResponseAsync7()
        {
            listBox12.Items.Clear();

            listBox13.Items.Clear();
            try
            {

                SqlConnection cnn = new SqlConnection(ConfigurationManager.ConnectionStrings["pliconnectionstring"].ConnectionString);
                SqlCommand cmd1;
                SqlDataReader reader;
                List<string> allurl = new List<string>();
                List<urlph> deturl = new List<urlph>();
                int ecount = 100;
                if (int.TryParse(textBox15.Text, out int outsete))
                    ecount = outsete;
                cnn.Close(); cnn.Open();
                cmd1 = new SqlCommand("select url,idphish from phishdata where isphish=-1 and checkphish<=@outsete", cnn);
                cmd1.Parameters.AddWithValue("@outsete", outsete);
                reader = cmd1.ExecuteReader();
                while (reader.Read())
                {
                    allurl.Add(reader["url"].ToString());
                    deturl.Add(new urlph { id = reader["idphish"].ToString(), url = reader["url"].ToString() });
                }
                cnn.Close();
                string noprocess = "";

                ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };
                HttpWebRequest request;
                Stream stream;
                WebResponse response;
                StreamReader strReader;
                string text;

                listBox12.Items.Clear();
                try
                {
                    listBox12.DataSource = allurl;
                }
                catch
                {

                }
                while (allurl.Count > 0 && start7)
                {
                    noprocess = allurl[0];
                    label31.Text = "Start proccess " + noprocess + " on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task7.Status.ToString();
                    try
                    {

                        request = (HttpWebRequest)HttpWebRequest.Create("https://phishtank.org/phish_detail.php?phish_id=" + deturl.First(x => x.url == noprocess).id.ToString());
                        request.UserAgent = useragentall;
                        if (int.TryParse(textBox5.Text, out int outin))
                            request.Timeout = outin;
                        else
                            request.Timeout = 10000;

                        response = request.GetResponse();
                        stream = response.GetResponseStream();
                        strReader = new StreamReader(stream);
                        text = await strReader.ReadToEndAsync();
                        if (text.Contains("<h3>Verified: <b>Is a phish</b></h3>"))
                        {
                            cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("update phishdata set isphish=1,checkphish=checkphish+1 where url=@url", cnn);
                            cmd1.Parameters.AddWithValue("@url", noprocess);
                            cmd1.ExecuteNonQuery();
                            cnn.Close();
                        }
                        else
                        {

                            cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("update phishdata set checkphish=checkphish+1 where url=@url", cnn);
                            cmd1.Parameters.AddWithValue("@url", noprocess);
                            cmd1.ExecuteNonQuery();
                            cnn.Close();
                        }
                        allurl.Remove(noprocess);
                    }
                    catch
                    {

                        cnn.Close(); cnn.Open();
                        cmd1 = new SqlCommand("update phishdata set checkphish=checkphish+1 where url=@url", cnn);
                        cmd1.Parameters.AddWithValue("@url", noprocess);
                        cmd1.ExecuteNonQuery();
                        cnn.Close();
                        allurl.Remove(noprocess);
                        listBox13.Items.Add("error in " + noprocess);

                    }
                    int sleep = 20000;
                    if (int.TryParse(textBox17.Text, out int outi))
                        sleep = outi;
                    else
                        sleep = 20000;
                    label31.Text = " Thread Sleep "+ sleep + " milisecound on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task7.Status.ToString();

                    await Task.Delay(sleep);

                }

                listBox12.DataSource = null;
            }
            catch (Exception ex)
            {

                listBox12.DataSource = null;
                listBox13.Items.Add("error in " + ex);

            }
        }

        private void button17_Click(object sender, EventArgs e)
        {

            if (!start8)
            {
                tokenSource8 = new CancellationTokenSource();
                CancellationToken ct = tokenSource8.Token;
                start8 = true;
                task8 = Task.Run(() => startwork8(), tokenSource8.Token);
                button17.Enabled = false;
                button16.Enabled = true;
            }
        }

        private void button16_Click(object sender, EventArgs e)
        {
            if (start8)
            {
                tokenSource8.Cancel();
                tokenSource8.Dispose();
                start8 = false;
                label37.Text = "Stop at " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss");

                listBox14.DataSource = null;
                button16.Enabled = false;
                button17.Enabled = true;
            }
        }


        public async Task startwork8()
        {
            while (start8)
            {
                label37.Text = "Start proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task8.Status.ToString();
                 GetResponseAsync8();

                label37.Text = "Compelet proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " And go to sleep for " + textBox20.Text + " minutes " + task8.Status.ToString();
                await Task.Delay(int.Parse(textBox20.Text) * 1000 * 60);

            }
        }
        public void GetResponseAsync8()
        {
            listBox14.Items.Clear();

            listBox15.Items.Clear();
            try
            {

                SqlConnection cnn = new SqlConnection(ConfigurationManager.ConnectionStrings["pliconnectionstring"].ConnectionString);
                SqlCommand cmd1;
                SqlDataReader reader;
                List<string> allurl = new List<string>();
                List<urlph> deturl = new List<urlph>();
                int ecount = 100;
                if (int.TryParse(textBox19.Text, out int outsete))
                    ecount = outsete;
                cnn.Close(); cnn.Open();
                cmd1 = new SqlCommand("select url,idphish from phishdata where dns is null and countns<=@outsete", cnn);
                cmd1.Parameters.AddWithValue("@outsete", outsete);
                reader = cmd1.ExecuteReader();
                while (reader.Read())
                {
                    allurl.Add(reader["url"].ToString());
                    deturl.Add(new urlph { id = reader["idphish"].ToString(), url = reader["url"].ToString() });
                }
                cnn.Close();
                string noprocess = "";

                ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };
                

                listBox14.Items.Clear();
                try
                {
                    listBox14.DataSource = allurl;
                }
                catch
                {

                }
                while (allurl.Count > 0 && start8)
                {
                    noprocess = allurl[0];
                    label37.Text = "Start proccess " + noprocess + " on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task8.Status.ToString();
                    try
                    {
                        StringBuilder stb = new StringBuilder();
                        foreach (IPAddress ip in  Dns.GetHostAddresses(noprocess.Replace(" ", "").Replace("\\", "/").Replace("http://", "").Replace("https://", "").Split('/')[0].Split('?')[0]))
                        {
                            stb.Append(ip.ToString()+Environment.NewLine);
                        }


                        if (stb.ToString()!="")
                        {
                            cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("update phishdata set dns=@dns,countns=countns+1 where url=@url", cnn);
                            cmd1.Parameters.AddWithValue("@url", noprocess);
                            cmd1.Parameters.AddWithValue("@dns", stb.ToString());
                            cmd1.ExecuteNonQuery();
                            cnn.Close();
                        }
                        else
                        {

                            cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("update phishdata set countns=countns+1 where url=@url", cnn);
                            cmd1.Parameters.AddWithValue("@url", noprocess);
                            cmd1.ExecuteNonQuery();
                            cnn.Close();
                        }
                        allurl.Remove(noprocess);
                    }
                    catch
                    {

                        cnn.Close(); cnn.Open();
                        cmd1 = new SqlCommand("update phishdata set countns=countns+1 where url=@url", cnn);
                        cmd1.Parameters.AddWithValue("@url", noprocess);
                        cmd1.ExecuteNonQuery();
                        cnn.Close();
                        allurl.Remove(noprocess);
                        listBox15.Items.Add("error in " + noprocess);

                    }
                    

                }

                listBox14.DataSource = null;
            }
            catch (Exception ex)
            {

                listBox14.DataSource = null;
                listBox15.Items.Add("error in " + ex);

            }
        }

        private void button19_Click(object sender, EventArgs e)
        {


            if (!start9)
            {
                tokenSource9 = new CancellationTokenSource();
                CancellationToken ct = tokenSource9.Token;
                start9 = true;
                task9 = Task.Run(() => startwork9(), tokenSource9.Token);
                button19.Enabled = false;
                button18.Enabled = true;
            }
        }

        private void button18_Click(object sender, EventArgs e)
        {

            if (start9)
            {
                tokenSource9.Cancel();
                tokenSource9.Dispose();
                start9 = false;
                label41.Text = "Stop at " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss");

                listBox16.DataSource = null;
                button18.Enabled = false;
                button19.Enabled = true;
            }
        }

        public async Task startwork9()
        {
            while (start9)
            {
                label41.Text = "Start proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task9.Status.ToString();
                await GetResponseAsync9();

                label41.Text = "Compelet proccess on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " And go to sleep for " + textBox22.Text + " minutes " + task9.Status.ToString();
                await Task.Delay(int.Parse(textBox22.Text) * 1000 * 60);

            }
        }
        public async Task GetResponseAsync9()
        {
            listBox16.Items.Clear();

            listBox17.Items.Clear();
            try
            {
                double fver = 537.38;
                SqlConnection cnn = new SqlConnection(ConfigurationManager.ConnectionStrings["pliconnectionstring"].ConnectionString);
                SqlCommand cmd1;
                SqlDataReader reader;
                List<string> allurl = new List<string>();
                List<urlph> deturl = new List<urlph>();
                int ecount = 100;
                if (int.TryParse(textBox21.Text, out int outsete))
                    ecount = outsete;
                cnn.Close(); cnn.Open();
                cmd1 = new SqlCommand("select url,idphish from phishdata where (ranksite is null or ranksite='') and checkrank<=@outsete order by id desc", cnn);
                cmd1.Parameters.AddWithValue("@outsete", outsete);
                reader = cmd1.ExecuteReader();
                while (reader.Read())
                {
                    allurl.Add(reader["url"].ToString());
                    deturl.Add(new urlph { id = reader["idphish"].ToString(), url = reader["url"].ToString() });
                }
                cnn.Close();
                string noprocess = "";

                ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };
                HttpWebRequest request;
                Stream stream;
                WebResponse response;
                StreamReader strReader;
                string text;
                StringBuilder stb = new StringBuilder();
                listBox16.Items.Clear();
                try
                {
                    listBox16.DataSource = allurl;
                }
                catch
                {

                }
                while (allurl.Count > 0 && start9)
                {
                    noprocess = allurl[0];
                    label41.Text = "Start proccess " + noprocess + " on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task9.Status.ToString();
                    int hasrank = 0;

                    stb = new StringBuilder();
                    SqlConnection cnn2 = new SqlConnection("Data Source=172.20.1.91,1433;Initial Catalog=pliwddata;Persist Security Info=True;User=mojtabasqldatabase; password=#P@rspaS##S");

                    cnn2.Open();
                    cmd1 = new SqlCommand("select ranksite from phishdata where url=@url", cnn2);
                    cmd1.Parameters.AddWithValue("@url", noprocess);
                    reader = cmd1.ExecuteReader();
                    while (reader.Read())
                    {
                        stb.Append(reader[0].ToString());
                        hasrank = 1;
                    }
                    cnn2.Close();
                    if (hasrank == 1&&stb.ToString()!="")
                    {
                        cnn.Close(); cnn.Open();
                        cmd1 = new SqlCommand("update phishdata set ranksite=@ranksite,checkrank=checkrank+1 where url=@url", cnn);
                        cmd1.Parameters.AddWithValue("@url", noprocess);
                        cmd1.Parameters.AddWithValue("@ranksite", stb.ToString());
                        cmd1.ExecuteNonQuery();
                        cnn.Close();
                        listBox17.Items.Add("add by 91 " + noprocess);
                        allurl.Remove(noprocess);

                    }
                    else
                    {
                        try
                        {

                            request = (HttpWebRequest)HttpWebRequest.Create("https://checkpagerank.net/index.php");
                            request.Method = "post";
                            var postData = "name=" + Uri.EscapeDataString(noprocess.Replace(" ", "").Replace("\\", "/").Replace("http://", "").Replace("https://", "").Split('/')[0].Split('?')[0]);
                            var data = Encoding.ASCII.GetBytes(postData);

                            request.Method = "POST";
                            request.ContentType = "application/x-www-form-urlencoded";
                            request.ContentLength = data.Length;
                            fver += 0.01;
                            request.UserAgent = useragentall.Replace("537.38",fver.ToString());

                            using (var stream1 = request.GetRequestStream())
                            {

                                stream1.Write(data, 0, data.Length);
                            }
                            if (int.TryParse(textBox5.Text, out int outin))
                                request.Timeout = outin;
                            else
                                request.Timeout = 10000;

                            response = request.GetResponse();
                            stream = response.GetResponseStream();
                            strReader = new StreamReader(stream);
                            text = await strReader.ReadToEndAsync();
                            stb = new StringBuilder();

                            int start = 0, end = 0;
                            try
                            {
                                start = 0;
                                end = 0;
                                start = text.IndexOf("Google PageRank: ", end);


                                end = text.IndexOf("</span>", start);
                                if (end > start & end != -1 & start != -1)
                                    stb.Append(text.Substring(start, end - start).Replace("<span style=\"color:#000099;\">", "") + Environment.NewLine);
                            }
                            catch
                            {

                            }

                            try
                            {
                                start = 0;
                                end = 0;
                                start = text.IndexOf("cPR Score: ", end);
                                end = text.IndexOf("</span>", start);

                                if (end > start & end != -1 & start != -1)
                                    stb.Append(text.Substring(start, end - start).Replace("<span style=\"color:#4D82F7;\">", "") + Environment.NewLine);
                            }
                            catch
                            {

                            }


                            try
                            {
                                start = 0;
                                end = 0;
                                start = text.IndexOf("<font>Domain Authority: ", end);
                                end = text.IndexOf("</font>", start);

                                if (end > start & end != -1 & start != -1)
                                    stb.Append(text.Substring(start, end - start) + Environment.NewLine);
                            }
                            catch
                            {

                            }
                            if (stb.ToString() != "")
                            {

                                listBox17.Items.Add("ok " +stb.ToString().Length+" "+ noprocess);
                                cnn.Close(); cnn.Open();
                                cmd1 = new SqlCommand("update phishdata set ranksite=@ranksite,checkrank=checkrank+1 where url=@url", cnn);
                                cmd1.Parameters.AddWithValue("@url", noprocess);
                                cmd1.Parameters.AddWithValue("@ranksite", stb.ToString());
                                cmd1.ExecuteNonQuery();
                                cnn.Close();
                            }
                            else
                            {

                                cnn.Close(); cnn.Open();
                                cmd1 = new SqlCommand("update phishdata set checkrank=checkrank+1 where url=@url", cnn);
                                cmd1.Parameters.AddWithValue("@url", noprocess);
                                cmd1.ExecuteNonQuery();
                                cnn.Close();
                            }
                            allurl.Remove(noprocess);
                        }
                        catch
                        {

                            cnn.Close(); cnn.Open();
                            cmd1 = new SqlCommand("update phishdata set checkrank=checkrank+1 where url=@url", cnn);
                            cmd1.Parameters.AddWithValue("@url", noprocess);
                            cmd1.ExecuteNonQuery();
                            cnn.Close();
                            allurl.Remove(noprocess);
                            listBox17.Items.Add("error in " + noprocess);

                        }
                        int sleep = 20000;
                        if (int.TryParse(textBox18.Text, out int outi))
                            sleep = outi;
                        else
                            sleep = 20000;
                        label41.Text = " Thread Sleep " + sleep + " milisecound on " + DateTime.Now.ToString("yyyy MM dd HH:mm:ss") + " ... " + task9.Status.ToString();

                        await Task.Delay(sleep);
                    }

                }

                listBox16.DataSource = null;
            }
            catch (Exception ex)
            {

                listBox16.DataSource = null;
                listBox17.Items.Add("error in " + ex);

            }
        }
    }
    public class urlph
    {
        public string url { get; set; }
        public string id { get; set; }
        public string detail { get; set; }

    }
}
