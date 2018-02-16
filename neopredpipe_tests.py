import unittest
import subprocess
import os

from postprocessing import DefineGenotypeFormat


class MyTestCase(unittest.TestCase):
    def test_genotypeformat_ad(self):
        line_ad = "line3\tnonsynonymous SNV\tPRAMEF20:NM_001099852:exon2:c.G247A:p.D83N,\tchr1\t13743058\t13743058\tG\tA\t0.1667\t19.4939\t26\tchr1\t13743058\t.\tG\tA\t19.4939\tPASS\tECNT=1;HCNT=22;MAX_ED=.;MIN_ED=.;NLOD=27.62;TLOD=10.35\tGT:AD:AF:ALT_F1R2:ALT_F2R1:FOXOG:QSS:REF_F1R2:REF_F2R1\t0/0:93,0:0.00:0:0:.:2406,0:49:44\t0/1:57,6:0.081:5:1:0.167:1457,187:32:25"
        self.assertEqual(('alldepths', 1), DefineGenotypeFormat(line_ad))

    def test_genotypeformat_a(self):
        line_a = "line3\tnonsynonymous SNV\tPRAMEF20:NM_001099852:exon2:c.G247A:p.D83N,\tchr1\t13743058\t13743058\tG\tA\t0.1667\t19.4939\t26\tchr1\t13743058\t.\tG\tA\t19.4939\tPASS\tNS=3;DISTR=|G|AG|G|;SB=1.0000	GT:A:GQ:SS:BCOUNT:DP\t0/0:G:100.0000:0:0,0,18,0:18\t0/1:AG:19.4939:2:4,0,15,0:19\t0/0:G:100.0000:0:0,0,26,0:26"
        self.assertEqual(('allele', 1), DefineGenotypeFormat(line_a))

    def test_genotypeformat_nv(self):
        line_nv = "line3\tnonsynonymous SNV\tPRAMEF20:NM_001099852:exon2:c.G247A:p.D83N,\tchr1\t13743058\t13743058\tG\tA\t0.1667\t19.4939\t26\tchr1\t13743058\t.\tG\tA\t19.4939\tMQ;badReads\tAC=5;AF=0.500;AN=10;BRF=0.97;FR=0.4556;HP=6;HapScore=2;MGOF=39;MMLQ=26;MQ=0.36;NF=4;NR=2;PP=111;QD=24.2952020912;SC=CAGATAGTGGAGGGGCTTACA;SbPval=0.65;Source=Platypus;TC=14;TCF=10;TCR=4;TR=6;WE=621651;WS=621636;set=FilteredInAll\tGT:GOF:GQ:NR:NV:PL\t0/1:4:15:2:1:33,0,15"
        self.assertEqual(('numvarreads', 4), DefineGenotypeFormat(line_nv))


    def test_main_platypus(self):
        os.system("rm ./test/Test_platypus.*")
        cmd = ['python', 'main_netMHCpan_pipe.py', '-I', './test/vcfs/', '-H', './test/hlatypes.txt', '-o', './test/',
               '-n', 'Test_platypus', '-c', '0', '1', '2', '3', '4', '-E', '8' ]
        runcmd = subprocess.Popen(cmd)
        runcmd.wait()
        with open('test/Test_platypus.neoantigens.txt', 'r') as testof:
            oflines = testof.readlines()
        self.assertEqual( ['1', '1', '0', '1', '0'] , oflines[0].split('\t')[1:6])

    def test_main_single_region(self):
        os.system("rm ./test/Test_single.*")
        cmd = ['python', 'main_netMHCpan_pipe.py', '-I', './test/vcfs/', '-H', './test/hlatypes.txt', '-o', './test/',
               '-n', 'Test_single', '-E', '8' ]
        runcmd = subprocess.Popen(cmd)
        runcmd.wait()
        with open('test/Test_single.neoantigens.summarytable.txt', 'r') as testof:
            oflines = testof.readlines()
        self.assertEqual( ['3', '2', '1'] , oflines[1].split('\t')[1:])


if __name__ == '__main__':
    unittest.main()
