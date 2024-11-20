TYPE_APPEAL_CHOICES = (
    (1, 'ОМС'),
    (2, 'ДМС'),
    (3, 'Платно'),
)
PLACE_CHOICES = (
    (1, 'На дому'),
    (2, 'ПМСП'),
    (3, 'Амбулаторно'),
    (4, 'Стационарно')
)

package_icd_field_names = [
    [
       'social_at_home_performed', 'social_primary_health_care_performed',
       'social_clinical_diagnostic_performed', 'social_hospital_performed'
    ],
    [
        'vhi_at_home_performed', 'vhi_primary_health_care_performed',
        'vhi_clinical_diagnostic_performed', 'vhi_hospital_performed'
    ],
    [
        'pay_at_home_performed', 'pay_primary_health_care_performed',
        'pay_clinical_diagnostic_performed', 'pay_hospital_performed'
    ]
]

package_service_field_names = [
        [
            'state_at_home__isnull',
            'state_primary_health_care__isnull',
            'state_clinical_diagnostic__isnull',
            'state_hospital__isnull'
        ],
        [
            'vhi_at_home_coefficient__isnull',
            'vhi_primary_health_care_coefficient__isnull',
            'vhi_clinical_diagnostic_coefficient__isnull',
            'vhi_hospital_coefficient__isnull'
        ],
        [
            'pay_at_home_coefficient__isnull',
            'pay_primary_health_care_coefficient__isnull',
            'pay_clinical_diagnostic_coefficient__isnull',
            'pay_hospital_coefficient__isnull'
        ]
    ]