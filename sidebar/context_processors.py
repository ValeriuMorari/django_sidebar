from .sidebar_constructor import DisPlayer
from .sidebar import menu


def sidebar(_):
    """
    Return context variable with sidebar html
    """

    return {
        'sidebar': DisPlayer([menu])
        #                             tool_config, infrastructure, issues, kpis, hep_kpis]),
        # 'sidebar': DisPlayer([menu, test_package, rtr, workflow, on_demand, ai, cancellation, nodes, tool_config,
        #                       infrastructure, issues]),
        # 'sidebar_staff': DisPlayer([menu, test_package, rtr, workflow, on_demand, ai, cancellation, nodes,
        #                             tool_config, infrastructure, issues, staff_kpis, hep_kpis]),
    }
