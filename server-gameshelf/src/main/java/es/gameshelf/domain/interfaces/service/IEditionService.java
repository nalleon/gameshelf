    package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.Edition;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IEditionService {
    Edition add(String name, String description);
    List<Edition> findAll();
    Edition findById(Integer id);
    Edition findByName(String name);
    boolean delete(Integer id);
    Edition update(Integer id, String name, String description);
}
