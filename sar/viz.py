#!/usr/bin/env python
'''
:mod:`sar.viz` is a module containing classes for visualizing sar logs.
'''

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

import numpy as np


class Visualization(object):
    PDF_OUTPUT = 0
    PNG_OUTPUT = 1
    SAR_TYPES = ['cpu', 'mem', 'io', 'paging', 'net']
    PLT_XTICK_LABEL_ROTATION = 'vertical'

    def __init__(self, sar_data, cpu=True, mem=True, paging=False, disk=False,
                 network=False):
        """Create a sar log visualization.

        Only CPU and memory usage charts are enabled by default.

        Args:
            sar_data (dict): Processed sar log from Parser
            cpu (:obj:`bool`, optional): Enable CPU usage charts
            mem (:obj:`bool`, optional): Enable memory usage cgarts
            paging (:obj:`bool`, optional): Enable paging activity charts
            disk (:obj:`bool`, optional): Enable disk usage charts
            network (:obj:`bool`, optional): Enable network usage charts
        """

        if not isinstance(sar_data, dict):
            raise 'Incompatible sar_data type: {}'.format(
                type(sar_data).__name__)

        self.sar_data = sar_data
        """dict: Processed sar logs"""

        self.enable_cpu = cpu
        self.enable_mem = mem
        self.enable_disk = disk
        self.enable_net = disk
        self.enable_paging = paging

        self.time_points = []
        """(:obj:`list` of :obj:`str`): time points which system activity was
            recorded"""

        self.x_data = []
        """(:obj:`list` of :obj:`int`): x axis data"""

        self.xticks = []
        """(:obj:`list` of :obj:`int`): x axis ticks"""

        self.xtick_labels = []
        """(:obj:`list` of :obj:`str`) x axis tick labels"""

        self.cpu_usage_usr = []
        self.cpu_usage_sys = []
        self.page_faults_per_sec = []
        self.major_page_faults_per_sec = []
        self.page_ins_per_sec = []
        self.page_outs_per_sec = []
        self.pct_mem_used = []
        self.mem_used_mb = []
        self.mem_cached_mb = []
        self.mem_buffer_mb = []
        self.kb_rcv_per_sec = {}
        self.kb_trans_per_sec = {}
        self.breads_per_sec = []
        self.bwrites_per_sec = []
        self.fig_height = 0
        self.num_plots = 0

        self._calculate_plot_height()
        self._preprocess_sar_data()

    def _calculate_plot_height(self):
        num_plots = 0

        if self.enable_cpu:
            num_plots += 1

        if self.enable_disk:
            num_plots += 1

        if self.enable_mem:
            num_plots += 2

        if self.enable_net:
            num_plots += 1

        if self.enable_paging:
            num_plots += 2

        self.num_plots = num_plots
        self.fig_height = num_plots * 4

    def _preprocess_sar_data(self):
        for t in Visualization.SAR_TYPES:
            if t in self.sar_data:
                time_points = self.sar_data[t].keys()
                time_points.sort()
                self.time_points = time_points
                break

        tp_count = len(time_points)
        xtick_label_stepsize = tp_count / 15
        self.x_data = range(tp_count)
        self.xticks = np.arange(0, tp_count, xtick_label_stepsize)
        self.xtick_labels = [time_points[i] for i in self.xticks]

        if self.enable_cpu:
            self.cpu_usage_sys = [self.sar_data['cpu'][tp]['all']['sys']
                                  for tp in self.time_points]
            self.cpu_usage_usr = [self.sar_data['cpu'][tp]['all']['usr']
                                  for tp in self.time_points]

        if self.enable_mem:
            self.pct_mem_used = [self.sar_data['mem'][tp]['memusedpercent'] / 1024
                                 for tp in self.time_points]
            self.mem_used_mb = [(self.sar_data['mem'][tp]['memused'] - (
                                 self.sar_data['mem'][tp]['memcache'] + self.sar_data['mem']
                                 [tp]['membuffer'])) / 1024 for tp in self.time_points]
            self.mem_cached_mb = [self.sar_data['mem'][tp]['memcache'] / 1024
                                  for tp in self.time_points]
            self.mem_buffer_mb = [self.sar_data['mem'][tp]['membuffer'] / 1024
                                  for tp in self.time_points]

        if self.enable_paging:
            self.page_faults_per_sec = [self.sar_data['paging'][tp]['fault']
                                        for tp in self.time_points]
            self.major_page_faults_per_sec = [self.sar_data['paging'][tp]['majflt']
                                              for tp in self.time_points]
            self.page_ins_per_sec = [self.sar_data['paging'][tp]['pgpgin']
                                     for tp in self.time_points]
            self.page_outs_per_sec = [self.sar_data['paging'][tp]['pgpgout']
                                      for tp in self.time_points]

        if self.enable_disk:
            self.breads_per_sec = [self.sar_data['io'][tp]['bread'] for tp in self.time_points]
            self.bwrites_per_sec = [self.sar_data['io'][tp]['bwrite'] for tp in self.time_points]

        if self.enable_net:
            net_data = self.sar_data['net']
            for tp in self.time_points:
                dp = net_data[tp]
                for iface in dp.keys():
                    if iface not in self.kb_rcv_per_sec:
                        self.kb_rcv_per_sec[iface] = [dp[iface]['rxkB']]
                    else:
                        self.kb_rcv_per_sec[iface].append(dp[iface]['rxkB'])

                    if iface not in self.kb_trans_per_sec:
                        self.kb_trans_per_sec[iface] = [dp[iface]['txkB']]
                    else:
                        self.kb_trans_per_sec[iface].append(dp[iface]['txkB'])

    def save(self, output_path, output_type=PDF_OUTPUT):
        plt_idx = 1
        fig = plt.figure()
        fig.set_figheight(self.fig_height)

        plt.clf()
        plt.subplots_adjust(wspace=1, hspace=1)

        if self.enable_cpu:
            plt.subplot(self.num_plots, 1, plt_idx)
            plt.xticks(self.xticks, self.xtick_labels,
                       rotation=Visualization.PLT_XTICK_LABEL_ROTATION)
            plt.plot(self.x_data, self.cpu_usage_usr, label='usr')
            plt.plot(self.x_data, self.cpu_usage_sys, label='sys')
            plt.xlabel('time')
            plt.ylabel('% usage')
            plt.title('CPU Usage')
            lg = plt.legend(frameon=False)
            lg_txts = lg.get_texts()
            plt.setp(lg_txts, fontsize=10)
            plt_idx += 1

        if self.enable_mem:
            plt.subplot(self.num_plots, 1, plt_idx)
            plt.xticks(self.xticks, self.xtick_labels,
                       rotation=Visualization.PLT_XTICK_LABEL_ROTATION)
            plt.plot(self.x_data, self.pct_mem_used, label='% mem used')
            plt.xlabel('time')
            plt.ylabel('% mem used')
            plt.title('Percentage of Memory Used')
            lg = plt.legend(frameon=False)
            lg_txts = lg.get_texts()
            plt.setp(lg_txts, fontsize=10)
            plt_idx += 1

            plt.subplot(self.num_plots, 1, plt_idx)
            plt.xticks(self.xticks, self.xtick_labels,
                       rotation=Visualization.PLT_XTICK_LABEL_ROTATION)
            plt.stackplot(self.x_data, self.mem_buffer_mb, self.mem_cached_mb, self.mem_used_mb,
                          colors=['lemonchiffon', 'navajowhite', 'sandybrown'])
            plt.xlabel('time')
            plt.ylabel('Mem Usage (MB)')
            plt.title('Memory Usage')

            # lc_handle = mpatches.Patch(color='lemonchiffon', label='Buffered Memory')
            # nw_handle = mpatches.Patch(color='navajowhite', label='Cached Memory')
            # sb_handle = mpatches.Patch(color='sandybrown', label='Used Memory')

            lg = plt.legend([mpatches.Patch(color='lemonchiffon'),
                             mpatches.Patch(color='navajowhite'),
                             mpatches.Patch(color='sandybrown')],
                            ['Buffered Memory', 'Cached Memory', 'Used Memory'])
            lg.get_frame().set_alpha(0.6)
            lg_txts = lg.get_texts()
            plt.setp(lg_txts, fontsize=10)
            plt_idx += 1

            fig.tight_layout()
            pp = PdfPages(output_path)
            pp.savefig()
            pp.close()
