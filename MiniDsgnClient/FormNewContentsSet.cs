using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace SyncBrowserClient
{
    public partial class FormNewContentsSet : Form
    {
        public FormNewContentsSet()
        {
            InitializeComponent();
        }

        public string ContentsSetName
        {
            get { return textBox1.Text; }
        }


    }
}
