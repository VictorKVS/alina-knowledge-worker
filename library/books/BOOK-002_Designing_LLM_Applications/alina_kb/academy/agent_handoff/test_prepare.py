import unittest
from prepare import prepare_package

REQUEST={"task_id":"T1","role":"OSINT","objective":"Check a public claim",
         "allowed_sensitivity":["public"],"max_items":10}
def rec(**kwargs):
    x={"source_id":"S1","permission":"approved","sensitivity":"public",
       "quality":"approved","statement":"Test assertion","source_spans":["p1"]}
    x.update(kwargs)
    return x

class HandoffTests(unittest.TestCase):
    def test_approved_source_passes(self):
        p=prepare_package(REQUEST,[rec()])
        self.assertEqual(p["handoff_status"],"READY")
        self.assertEqual(p["knowledge_items"][0]["source_spans"],["p1"])

    def test_unknown_permission_excluded(self):
        p=prepare_package(REQUEST,[rec(permission="unknown")])
        self.assertEqual(p["handoff_status"],"BLOCKED")
        self.assertEqual(p["knowledge_items"],[])

    def test_role_clearance(self):
        p=prepare_package(REQUEST,[rec(sensitivity="confidential")])
        self.assertEqual(len(p["knowledge_items"]),0)

    def test_duplicate_provenance_kept(self):
        p=prepare_package(REQUEST,[rec(),rec(source_id="S2",same_content=True,lineage_root="S1")])
        self.assertEqual(len(p["knowledge_items"]),1)
        self.assertEqual(p["evidence_groups"][0]["source_ids"],["S1","S2"])

    def test_review_quality(self):
        p=prepare_package(REQUEST,[rec(quality="unknown")])
        self.assertEqual(p["source_decisions"][0]["decision"],"REVIEW")

    def test_revision_kept(self):
        p=prepare_package(REQUEST,[rec(is_revision=True)])
        self.assertEqual(p["source_decisions"][0]["decision"],"NEW_VERSION")

if __name__=="__main__": unittest.main()
