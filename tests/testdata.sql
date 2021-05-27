SET FOREIGN_KEY_CHECKS = 0;

-- Tapir Users
INSERT INTO `tapir_users` VALUES (246231,'Brandon','Barker','',1,1,'no-mail@example.com',8,0,2,1384185389,'dedicated','',0,0,0,1,1,0,0,0,0,'cpe-24-59.res.rr.com.1372902602452690',0,0);


INSERT INTO `arXiv_moderators` VALUES (246231,'q-bio','CB','0','0','0','0','0');
INSERT INTO `arXiv_moderators` VALUES (246231,'q-bio','NC','0','0','0','0','0');
INSERT INTO `arXiv_moderators` VALUES (246231,'q-bio', '','0','0','0','0','0');


INSERT INTO `tapir_users` VALUES (246232,'Lo','Jack','',1,1,'other-no-mail@example.com',8,0,2,1384185389,'net','',0,0,0,1,1,0,0,0,0,'cpe-24-59.com.1372902602452690',0,0);

INSERT INTO `arXiv_moderators` VALUES (246232,'q-bio','NC','0','0','0','0','0');

-- Tapir Nicknames
INSERT INTO `tapir_nicknames` VALUES (246208,'bbarker',246231,1,1,0,0,1);
INSERT INTO `tapir_nicknames` VALUES (246209,'lowjack',246232,1,1,0,0,1);

-- Submissions
INSERT INTO `arXiv_submissions` 
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`) 
VALUES 
(1137914,NULL,NULL,NULL,1,1,1,1,4 /* stage */,246231,'Brandon Barker','beb82@cornell.edu','2015-10-12 17:11:21','2015-10-12 21:58:44',1 /* status */,NULL,0,'2015-11-17 15:11:21',NULL,2848951,'pdf','1',0,0,'MPI 3 One more time','Brandon Barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'The Message Passing Interface, version three point zero.','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'new',NULL,NULL,0,'128.84.31.207','bbsurfacepro3.tc.cornell.edu','/users/e-prints/arXivLib/t/user_data/Kubla_Khan.pdf',NULL,0,NULL);

INSERT INTO `arXiv_submission_category` 
(`submission_id`, `category`, `is_primary`, `is_published`) 
VALUES (1137914,'q-bio.CB',1,0);


INSERT INTO `arXiv_submission_abs_classifier_data`
( `submission_id`, `json`, `last_update`, `status`, `message`,
`is_oversize`, `suggested_primary`, `suggested_reason`,
`autoproposal_primary`, `autoproposal_reason`,
`classifier_service_version`, `classifier_model_version`)
VALUES(
1137914,
'{"classifier":[{"category":"hep-ph","probability":0.97},{"category":"hep-ex","probability":0.65},{"category":"hep-th","probability":0.02},{"category":"nucl-ex","probability":0.01},{"category":"nucl-th","probability":0.01}],"service":"fb-abs"}',
'2021-04-13 12:49:38', 'success', NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL);


INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`)
VALUES
(1137933,NULL,NULL,NULL,1,1,1,1,5,246231,'Brandon Barker','beb82@cornell.edu','2015-11-17 15:07:23','2015-11-17 15:11:21',1 /*status*/,NULL,0,NULL,NULL,500,'tex','1',0,0,'A very simple LaTeX example','Brandon Barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'A very simple LaTeX example.','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'new',0,0,0,'10.128.128.241','dhcp-gs-241.eduroam.cornell.edu','/users/e-prints/arXivLib/t/user_data/very_simple_1137933.gz',NULL,0,NULL);


INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES (1137933,'q-bio.NC',1,0);



INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`, is_locked)
VALUES
(100430 ,NULL,NULL,NULL,1,1,1,1,5,246231,'Brandon Barker','beb82@cornell.edu','2015-11-17 15:07:23','2015-11-17 15:11:21',1 /*status*/,NULL,0,'2015-11-17 15:11:21',NULL,500,'tex','1',0,0,'A very simple LaTeX example','Brandon Barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'A very simple LaTeX example.','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'new',0,0,0,'10.128.128.241','dhcp-gs-241.eduroam.cornell.edu','/users/e-prints/arXivLib/t/user_data/very_simple_1137933.gz',NULL,0,NULL, 1);


INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES (100430,'q-bio.NC',1,0);



INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`)
VALUES
(1137931,NULL,NULL,NULL,1,1,1,1,5,246231,'Brandon Barker','beb82@cornell.edu','2015-11-16 18:04:31','2015-11-17 13:37:25',1/*status*/,NULL,0,'2015-11-16 19:50:55',NULL,998628,'pdftex','',0,0,'First timeout fail case','Brandon Barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'First timeout fail case','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'new',NULL,NULL,0,'128.84.31.207','bbsurfacepro3.tc.cornell.edu','/users/e-prints/arXivLib/t/user_data/extraction_timeout1_1137931.tar.gz',NULL,1,NULL);


INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES (1137931,'q-bio.GN',1,0);



INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`)
VALUES
(1137932,NULL,NULL,NULL,1,1,1,1,5,246231,'Brandon Barker','beb82@cornell.edu','2015-11-16 19:58:40','2015-11-17 14:15:41',0,NULL,0,NULL,NULL,1502662,'pdftex','',0,0,'Second timeout test case','Brandon barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Second timeout test case','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'new',0,0,0,'128.84.31.207','bbsurfacepro3.tc.cornell.edu','/users/e-prints/arXivLib/t/user_data/extraction_timeout1_1137932.tar.gz',NULL,0,NULL);


INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES (1137932,'q-bio.GN',1,0);
  
