using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Configuration;
using System.Xml;

namespace SyncBrowserClient
{
    public partial class Form1 : Form
    {
        int combo1SelIndex = -1;
        int combo2SelIndex = -1;
        Dictionary<string, ContentsSet> dicContent = new Dictionary<string, ContentsSet>();
        ContentsSet contentCurrent = null;
        ContentsSet contentSelected = new ContentsSet();
        int contentIndex = -1;
        string dataFileName = "";
        int tickPast = 0;

        private class ContentsSet
        {
            public string name = "";
            public List<string> lsURL = new List<string>();
            public int interval = 60;
        }

        public Form1()
        {
            InitializeComponent();

        }

        private void comboBox2_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (comboBox2.SelectedIndex == 0)
            {
                FormNewContentsSet fm = new FormNewContentsSet();
                if (fm.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    ContentsSet content = new ContentsSet();
                    content.name = fm.ContentsSetName;
                    dicContent.Add(content.name, content);
                    int posNewContent = comboBox2.Items.Add(content.name);
                    //comboBox2.Select(posNewContent, 1);
                    comboBox2.SelectedIndex = posNewContent;
                    SaveContentList();
                }
                ContentsSet content = new ContentsSet();
                content.name = fm.ContentsSetName;
                dicContent.Add(content.name, content);
                int posNewContent = comboBox2.Items.Add(content.name);
                //comboBox2.Select(posNewContent, 1);
                comboBox2.SelectedIndex = posNewContent;
                SaveContentList();
            }
            else
            {
                combo2SelIndex = comboBox2.SelectedIndex;
                string name = (string)comboBox2.Items[combo2SelIndex];
                ContentsSet content = dicContent[name];
                listView1.Items.Clear();
                foreach (string url in content.lsURL)
                {
                    listView1.Items.Add(url);
                }
                contentSelected = content;
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (contentSelected != null)
            {
                contentCurrent = contentSelected;
                contentIndex = 0;
                OpenContent(contentIndex);
                tickPast = 0;

                timer1.Start();
            }
        }

        private void comboBox1_KeyUp(object sender, KeyEventArgs e)
        {
            if(e.KeyCode == Keys.Enter)
            {
                comboBox1.Items.Add(comboBox1.Text);
                SaveHostList();
            }
            else if (e.KeyCode == Keys.Delete)
            {
                if (combo1SelIndex != -1)
                {
                    object obj = comboBox1.Items[combo1SelIndex];
                    comboBox1.Items.Remove(obj);
                    SaveHostList();
                }
            }
        }

        private void comboBox2_KeyUp(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                comboBox2.Items.Add(comboBox2.Text);
                //SaveHostList();
            }
            else if (e.KeyCode == Keys.Delete)
            {
                if (combo2SelIndex != -1)
                {
                    object obj = comboBox2.Items[combo2SelIndex];
                    comboBox2.Items.Remove(obj);
                    //SaveHostList();
                }
            }
        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            combo1SelIndex = comboBox1.SelectedIndex;
        }

        private void textBox1_KeyUp(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                webBrowser1.Navigate(textBox1.Text);
            }
        }

        private void button3_Click(object sender, EventArgs e)
        {
            string url = textBox1.Text;
            listView1.Items.Add(url);
            contentSelected.lsURL.Add(url);

            string name = contentSelected.name;
            ContentsSet temp = dicContent[name];
            if (temp.lsURL.Count != contentSelected.lsURL.Count)
                MessageBox.Show("error");

            SaveContentList();

        }

        private void Form1_Load(object sender, EventArgs e)
        {
            /*
            // Get the configuration  
            // that applies to the all user.
            Configuration appConfig =
              ConfigurationManager.OpenExeConfiguration(
               ConfigurationUserLevel.None);
            string imageNodeName = appConfig.AppSettings.Settings["ImageNodeName"].Value;
             */
            string[] args = Environment.GetCommandLineArgs();
            if (args.Length == 1)
                dataFileName = "default.xml";
            else
                dataFileName = args[1];

            try
            {
                System.Xml.XmlDocument doc = new System.Xml.XmlDocument();
                doc.Load(dataFileName);
                XmlNodeList ContentsSetLists = doc.GetElementsByTagName("ContentsSetList");
                XmlNode contentsSetListNode = ContentsSetLists[0];
                foreach (XmlNode contentsSetNode in contentsSetListNode.ChildNodes)
                {
                    if (contentsSetNode.Name == "ContentsSet")
                    {
                        ContentsSet contentsSet = new ContentsSet();
                        contentsSet.name = contentsSetNode.Attributes["name"].Value;
                        contentsSet.interval = Convert.ToInt32(contentsSetNode.Attributes["interval"].Value);
                        foreach (XmlNode cNode in contentsSetNode.ChildNodes)
                        {
                            if (cNode.Name.ToUpper() == "URL")
                            {
                                XmlCDataSection cdata_url = (XmlCDataSection)cNode.FirstChild;
                                contentsSet.lsURL.Add(cdata_url.Data);
                            }
                        }
                        dicContent.Add(contentsSet.name, contentsSet);
                        comboBox2.Items.Add(contentsSet.name);
                    }
                }

                XmlNodeList hostsNodes = doc.GetElementsByTagName("Hosts");
                foreach (XmlNode hostNode in hostsNodes[0])
                {
                    if (hostNode.Name == "Host")
                    {
                        string hostname = hostNode.Attributes["hostname"].Value;
                        comboBox1.Items.Add(hostname);
                    }
                }

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }

            listView1.Columns[0].Width = listView1.Width - 4;

        }

        private void listView1_MouseDoubleClick(object sender, MouseEventArgs e)
        {
            int sel = listView1.SelectedIndices[0];
            string url = listView1.Items[sel].Text;
            webBrowser1.Navigate(url);
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            tickPast += timer1.Interval/1000;
            if (contentCurrent != null && contentCurrent.interval <= tickPast)
            {
                if (-1 < contentIndex)
                    contentIndex++;
                if (contentIndex >= contentCurrent.lsURL.Count)
                    contentIndex = 0;
                OpenContent(contentIndex);
                tickPast = 0;
            }
        }

        private void OpenContent(int index)
        {
            foreach (string host in comboBox1.Items)
            {
                /*
                SyncBrowser.Service1Client cl = new SyncBrowser.Service1Client();
                string uri = string.Format("http://{0}:9099/SyncBrowser/SyncBrowser/", host);
                cl.Endpoint.Address = new System.ServiceModel.EndpointAddress(uri);
                cl.OpenUrl(comboBox2.Text);
                 */
                if (index > -1 && index < contentCurrent.lsURL.Count)
                {
                    string url = contentCurrent.lsURL[index];
                    webBrowser1.Navigate(url);
                    try
                    {
                        minidsgnsvc.my_dispatcherPortTypeClient cl = new minidsgnsvc.my_dispatcherPortTypeClient();
                        string uri = string.Format("http://{0}:8008/", host);
                        cl.Endpoint.Address = new System.ServiceModel.EndpointAddress(uri);
                        cl.Open(url);
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine(e.Message);
                    }
                }
            }
        }

        private void SaveContentList()
        {
            try
            {
                System.Xml.XmlDocument doc = new System.Xml.XmlDocument();
                doc.Load(dataFileName);
                
                XmlNodeList ContentsSetLists = doc.GetElementsByTagName("ContentsSetList");
                XmlNode contentsSetListNode = ContentsSetLists[0];
                contentsSetListNode.RemoveAll();
                foreach (ContentsSet contentsSet in dicContent.Values)
                {
                    XmlNode newContentsSetNode = doc.CreateNode(XmlNodeType.Element, "ContentsSet", "");
                    XmlAttribute attrName = doc.CreateAttribute("name");
                    attrName.Value = contentsSet.name;
                    newContentsSetNode.Attributes.Append(attrName);
                    XmlAttribute attrInterval = doc.CreateAttribute("interval");
                    attrInterval.Value = contentsSet.interval.ToString();
                    newContentsSetNode.Attributes.Append(attrInterval);
                    foreach (string url in contentsSet.lsURL)
                    {
                        XmlNode newUrlNode = doc.CreateNode(XmlNodeType.Element, "URL", "");
                        XmlCDataSection cdata = doc.CreateCDataSection(url);
                        newUrlNode.AppendChild(cdata);
                        newContentsSetNode.AppendChild(newUrlNode);
                    }
                    contentsSetListNode.AppendChild(newContentsSetNode);
                }
                doc.Save(dataFileName);
                
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }

        }
        private void SaveHostList()
        {
            try
            {
                System.Xml.XmlDocument doc = new System.Xml.XmlDocument();
                doc.Load(dataFileName);

                XmlNodeList hostsNodes = doc.GetElementsByTagName("Hosts");
                XmlNode hostsNode = hostsNodes[0];
                hostsNode.RemoveAll();
                foreach (string hostname in comboBox1.Items)
                {
                    XmlNode newHostNode = doc.CreateNode(XmlNodeType.Element, "Host", "");
                    XmlAttribute attr = doc.CreateAttribute("hostname");
                    attr.Value = hostname;
                    newHostNode.Attributes.Append(attr);
                    hostsNode.AppendChild(newHostNode);
                }
                doc.Save(dataFileName);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }

        }

        private void comboBox2_DrawItem(object sender, DrawItemEventArgs e)
        {
            if (e.Index == -1)
            {
                return;
            }

            if (e.Index != combo2SelIndex)
            {
                e.Graphics.DrawString(
                    comboBox2.Items[e.Index].ToString(),
                    this.Font,
                    Brushes.Black,
                    new Point(e.Bounds.X + e.Bounds.Height, e.Bounds.Y));
                return;
            }
            else
            {
                e.Graphics.DrawString(
                    comboBox2.Items[e.Index].ToString(),
                    this.Font,
                    Brushes.Black,
                    new Point(e.Bounds.X + e.Bounds.Height, e.Bounds.Y));
                e.Graphics.DrawImage(
                    SyncBrowserClient.Properties.Resources.Checked,
                    new Point(e.Bounds.X, e.Bounds.Y)
                    );
                return;

            }
        }
    }
}
