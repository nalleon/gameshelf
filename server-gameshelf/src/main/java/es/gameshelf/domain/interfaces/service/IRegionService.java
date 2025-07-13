package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.Region;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IRegionService {
    Region add(String name, String initials);
    List<Region> findAll();
    Region findById(Integer id);
    Region findByName(String name);
    boolean delete(Integer id);
    Region update(String name, String initials);
}
